import argparse
import os
from typing import List, Iterable, Union

from defusedxml import ElementTree
from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from idc.api import ObjectDetectionData, locate_image
from idc.api import Reader


class VOCObjectDetectionReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 image_rel_path: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param image_rel_path: the relative path to apply to "folder" for locating the images
        :type image_rel_path: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.image_rel_path = image_rel_path
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-voc-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box from the associated .xml file in PASCAL VOC format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the XML file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the XML files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-r", "--image_rel_path", type=str, help="The relative path to use for the 'folder' property to locate the images.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.image_rel_path = ns.image_rel_path

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.image_rel_path is None:
            self.image_rel_path = ""
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.xml")

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        xml = ElementTree.parse(self.session.current_input)
        if len(self.image_rel_path) > 0:
            img = os.path.join(
                os.path.dirname(self.session.current_input),
                self.image_rel_path,
                xml.findtext("folder"),
                xml.findtext("filename")
            )
        else:
            img = os.path.join(
                os.path.dirname(self.session.current_input),
                xml.findtext("folder"),
                xml.findtext("filename")
            )
        if not os.path.exists(img):
            self.logger().warning("Failed to locate image based on information in XML.")
            img = locate_image(self.session.current_input)
            if img is None:
                self.logger().warning("No corresponding image found for: %s" % self.session.current_input)
                self._current_input = None
                yield None

        lobjs = LocatedObjects()
        for obj in xml.findall("object"):
            label = obj.findtext("name")

            # Get the bounding box XML element
            bbox = obj.find("bndbox")

            # Get the boundary co-ordinates
            x_min = int(bbox.findtext("xmin"))
            x_max = int(bbox.findtext("xmax"))
            y_min = int(bbox.findtext("ymin"))
            y_max = int(bbox.findtext("ymax"))

            meta = dict()
            meta["type"] = label
            lobj = LocatedObject(x_min, y_min, x_max - x_min + 1, y_max - y_min + 1, **meta)
            lobjs.append(lobj)

        yield ObjectDetectionData(source=str(img), annotation=lobjs)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
