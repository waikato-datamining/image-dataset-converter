import argparse
import json
import os.path
from typing import List, Iterable, Union, Dict

from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Point, Polygon
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData
from idc.api import Reader


class COCOObjectDetectionReader(Reader, PlaceholderSupporter):

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
        return "from-coco-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box or polygon definitions from the associated .json file in MS COCO format."

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

    def _create_lookup(self, data: Dict, key: str, key_name: str) -> Dict:
        """
        Generates a lookup from the data.

        :param data: the data to use
        :type data: dict
        :param key: the name of the key to generate the lookup for
        :type key: str
        :return: the lookup (id -> name)
        :rtype: dict
        """
        if key not in data:
            raise Exception("No '%s' available!" % key)
        result = dict()

        for item in data[key]:
            result[item["id"]] = item[key_name]

        return result

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        # load annotations
        with open(self.session.current_input, "r") as fp:
            data = json.load(fp)

        categories = self._create_lookup(data, "categories", "name")
        license_names = self._create_lookup(data, "licenses", "name")
        license_urls = self._create_lookup(data, "licenses", "url")
        images = self._create_lookup(data, "images", "file_name")
        image_licenses = self._create_lookup(data, "images", "license")

        for image_id in images:
            filename = images[image_id]
            license_name = None
            license_url = None
            if image_id in image_licenses:
                license_id = image_licenses[image_id]
                if license_id in license_names:
                    license_name = license_names[license_id]
                if len(license_name) == 0:
                    license_name = None
                if license_id in license_urls:
                    license_url = license_urls[license_id]
                    if len(license_url) == 0:
                        license_url = None
            img = os.path.join(os.path.dirname(self.session.current_input), filename)
            if not os.path.exists(img):
                self.logger().error("Image file not found for ID #%d: %s" % (image_id, img))
                continue

            lobjs = LocatedObjects()
            file_meta = dict()
            file_meta["image_id"] = image_id
            file_meta["file"] = self.session.current_input
            if license_name is not None:
                file_meta["license_name"] = license_name
            if license_url is not None:
                file_meta["license_url"] = license_url
            for annotation in data["annotations"]:
                if image_id != annotation["image_id"]:
                    continue
                category_id = annotation["category_id"]
                meta = dict()
                meta["type"] = categories[category_id]
                x, y, w, h = annotation["bbox"]
                lobj = LocatedObject(x, y, w, h, **meta)
                lobjs.append(lobj)
                if annotation["iscrowd"] == 0:
                    segmentation = annotation["segmentation"]
                    if isinstance(segmentation, list) and (len(segmentation) > 0):
                        if len(segmentation) > 1:
                            self.logger().warning("More than one polygon defined for annotation id #%d, only using first!" % annotation["id"])
                        for subsegmentation in segmentation:
                            points = []
                            i = 0
                            while i < len(subsegmentation) - 1:
                                points.append(Point(int(subsegmentation[i]), int(subsegmentation[i+1])))
                                i += 2
                            polygon = Polygon(*points)
                            lobj.set_polygon(polygon)
                            # we only process one
                            break

            yield ObjectDetectionData(source=str(img), annotation=lobjs, metadata=file_meta)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
