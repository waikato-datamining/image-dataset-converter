import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from seppl.io import Filter
from idc.api import ObjectDetectionData, flatten_list, make_list


class DimensionDiscarder(Filter):
    """
    Removes annotations which fall outside certain dimensional limits.
    """

    def __init__(self, min_width: int = None, min_height: int = None, 
                 max_width: int = None, max_height: int = None,
                 min_area: int = None, max_area: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param min_width: the minimum width for annotations, ignored if None
        :type min_width: int
        :param min_height: the minimum height for annotations, ignored if None
        :type min_height: int
        :param max_width: the maximum width for annotations, ignored if None
        :type max_width: int
        :param max_height: the maximum height for annotations, ignored if None
        :type max_height: int
        :param min_area: the minimum area (polygon if available or bbox) for annotations, ignored if None
        :type min_area: int
        :param max_area: the maximum area (polygon if available or bbox) for annotations, ignored if None
        :type max_area: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.min_area = min_area
        self.max_area = max_area

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "dimension-discarder"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Removes annotations which fall outside certain dimensional limits."

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
        parser.add_argument("--min_width", type=int, default=None, help="The minimum width for annotations", required=False)
        parser.add_argument("--min_height", type=int, default=None, help="The minimum height for annotations", required=False)
        parser.add_argument("--max_width", type=int, default=None, help="The maximum width for annotations", required=False)
        parser.add_argument("--max_height", type=int, default=None, help="The maximum height for annotations", required=False)
        parser.add_argument("--min_area", type=int, default=None, help="The minimum area for annotations (polygon if available, otherwise bbox)", required=False)
        parser.add_argument("--max_area", type=int, default=None, help="The maximum area for annotations (polygon if available, otherwise bbox)", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.min_width = ns.min_width
        self.min_height = ns.min_height
        self.max_width = ns.max_width
        self.max_height = ns.max_height
        self.min_area = ns.min_area
        self.max_area = ns.max_area

    def _should_discard_located_object(self, located_object: LocatedObject) -> bool:
        """
        Decides if the located object should be discarded.

        :param located_object:  The located object.
        :return:                True if it should be discarded,
                                False if it should be kept.
        """
        # Min width check
        if self.min_width is not None and located_object.width < self.min_width:
            self.logger().debug("Width too small: %d < %d" % (located_object.width, self.min_width))
            return True

        # Max width check
        if self.max_width is not None and located_object.width > self.max_width:
            self.logger().debug("Width too large: %d > %d" % (located_object.width, self.max_width))
            return True

        # Min height check
        if self.min_height is not None and located_object.height < self.min_height:
            self.logger().debug("Height too small: %d < %d" % (located_object.height, self.min_height))
            return True

        # Max height check
        if self.max_height is not None and located_object.height > self.max_height:
            self.logger().debug("Height too large: %d > %d" % (located_object.height, self.max_height))
            return True

        # Return before calculating the area if there are no area bounds
        if self.min_area is None and self.max_area is None:
            return False

        # Calculate the area of the object
        area = (
            located_object.get_actual_polygon().area()
            if located_object.has_polygon()
            else located_object.get_actual_rectangle().area()
        )

        # Min area check
        if self.min_area is not None and area < self.min_area:
            self.logger().debug("Area too small: %d < %d" % (area, self.min_area))
            return True

        # Max area check
        if self.max_area is not None and area > self.max_area:
            self.logger().debug("Area too large: %d > %d" % (area, self.max_area))
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
