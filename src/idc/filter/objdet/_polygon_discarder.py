import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from seppl.io import Filter
from idc.api import ObjectDetectionData, flatten_list, make_list


class PolygonDiscarder(Filter):
    """
    Removes polygons that fall outside the specified point limits (skips annotations with no polygons).
    """

    def __init__(self, min_points: int = None, max_points: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param min_points: the minimum number of points in the polygon, ignored if None
        :type min_points: int
        :param max_points: the maximum number of points in the polygon, ignored if None
        :type max_points: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.min_points = min_points
        self.max_points = max_points

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "polygon-discarder"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Removes polygons that fall outside the specified point limits (skips annotations with no polygons)."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--min_points", type=int, default=None, help="The minimum number of points", required=False)
        parser.add_argument("-M", "--max_points", type=int, default=None, help="The maximum number of points", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.min_points = ns.min_points
        self.max_points = ns.max_points

    def _should_discard_located_object(self, located_object: LocatedObject) -> bool:
        """
        Decides if the located object should be discarded.

        :param located_object:  The located object.
        :return:                True if it should be discarded,
                                False if it should be kept.
        """
        if not located_object.has_polygon():
            return False

        poly_x = located_object.get_polygon_x()

        # Min points
        if self.min_points is not None and len(poly_x) < self.min_points:
            self.logger().debug("Too few points: %d < %d" % (len(poly_x), self.min_points))
            return True

        # Max points
        if self.max_points is not None and len(poly_x) > self.max_points:
            self.logger().debug("Too many points: %d > %d" % (len(poly_x), self.max_points))
            return True

        return False

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann = LocatedObjects((located_object
                                  for located_object in item.annotation
                                  if not self._should_discard_located_object(located_object)))
            if len(ann) != len(item.annotation):
                item = item.duplicate(annotation=ann)
            result.append(item)

        return flatten_list(result)
