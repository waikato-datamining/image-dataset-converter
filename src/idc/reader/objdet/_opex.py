import argparse
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from wai.common.geometry import Point, Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from opex import ObjectPredictions
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from idc.api import ObjectDetectionData, locate_image
from idc.api import Reader


class OPEXObjectDetectionReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-opex-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box and/or polygon definitions from the associated .json file in OPEX format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the JSON file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the JSON files to use; " + placeholder_list(obj=self), required=False, nargs="*")
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
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.json")

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        img = locate_image(self.session.current_input)
        if img is None:
            self.logger().warning("No corresponding image found for: %s" % self.session.current_input)
            yield None

        preds = ObjectPredictions.load_json_from_file(self.session.current_input)

        lobjs = LocatedObjects()
        for obj in preds.objects:
            meta = dict()
            if obj.score is not None:
                meta["score"] = obj.score
            if obj.label is not None:
                meta["type"] = obj.label
            if isinstance(obj.meta, dict):
                for k, v in obj.meta.items():
                    meta[k] = v
            lobj = LocatedObject(obj.bbox.left, obj.bbox.top, obj.bbox.right - obj.bbox.left + 1, obj.bbox.bottom - obj.bbox.top + 1, **meta)
            lpoints = []
            for point in obj.polygon.points:
                lpoint = Point(point[0], point[1])
                lpoints.append(lpoint)
            lobj.set_polygon(Polygon(*lpoints))
            lobjs.append(lobj)

        # meta-data?
        meta = dict()
        meta["id"] = preds.id
        if preds.timestamp is not None:
            meta["timestamp"] = preds.timestamp
        if isinstance(preds.meta, dict):
            meta = dict()
            for k, v in preds.meta.items():
                meta[k] = v

        yield ObjectDetectionData(source=img, annotation=lobjs, metadata=meta)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
