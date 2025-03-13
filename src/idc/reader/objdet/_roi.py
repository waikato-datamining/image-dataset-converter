import argparse
import csv
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from idc.api import ObjectDetectionData, locate_image
from idc.api import Reader


class ROIObjectDetectionReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 suffix: str = "-rois.csv", logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param suffix: the suffix of the ROI CSV files (eg -rois.csv)
        :type suffix: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.suffix = suffix
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-roicsv-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box and/or polygon definitions from the associated ROI .csv file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the CSV file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the CSV files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-s", "--suffix", metavar="SUFFIX", type=str, default="-rois.csv", help="The suffix used by the ROI CSV files.", required=False)
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
        self.suffix = ns.suffix

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
        if self.suffix is None:
            raise Exception("No suffix defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.csv")

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self.finalize()

        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        image = locate_image(self.session.current_input, suffix=self.suffix)
        if image is None:
            self.logger().warning("No associated image found: %s" % self._current_input)
            yield None

        with open(self.session.current_input, "r") as fp:
            reader = csv.DictReader(fp)

            annotations = LocatedObjects()
            for row in reader:
                if "x0" in row:
                    x0 = int(float(row["x0"]))
                    y0 = int(float(row["y0"]))
                    x1 = int(float(row["x1"]))
                    y1 = int(float(row["y1"]))
                else:
                    x0 = int(float(row["x"]))
                    y0 = int(float(row["y"]))
                    w = int(float(row["w"]))
                    h = int(float(row["h"]))
                    x1 = x0 + w - 1
                    y1 = y0 + h - 1
                meta = dict()
                fields = ["score", "label", "label_str", "minrect_w", "minrect_h"]
                for field in fields:
                    if field in row:
                        value = row[field]
                        if len(value) > 0:
                            if field in ["score", "minrect_w", "minrect_h"]:
                                value = float(value)
                            elif field in ["label"]:
                                value = int(value)
                            meta[field] = value
                if "label_str" in row:
                    meta["type"] = row["label_str"]
                poly = None
                if ("poly_x" in row) and ("poly_y" in row):
                    points = []
                    px_list = row["poly_x"].split(",")
                    py_list = row["poly_y"].split(",")
                    for x, y in zip(px_list, py_list):
                        points.append(Point(int(float(x)), int(float(y))))
                    poly = Polygon(*points)

                obj = LocatedObject(x=x0, y=y0, width=x1-x0+1, height=y1-y0+1, meta=meta)
                if poly is not None:
                    obj.set_polygon(poly)
                annotations.append(obj)

            if len(annotations) == 0:
                annotations = None

        self._current_input = None

        yield ObjectDetectionData(source=image, annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
