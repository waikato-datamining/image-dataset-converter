import argparse
import copy
from typing import List, Tuple

from shapely import simplify, Polygon
from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Point as WaiPoint, Polygon as WaiPolygon

from seppl.io import Filter
from idc.api import ObjectDetectionData, flatten_list, make_list, locatedobject_polygon_to_shapely


class PolygonSimplifier(Filter):
    """
    Simplifies polygons according to the tolerance parameter: the smaller the tolerance, the closer to the original.
    """

    def __init__(self, tolerance: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param tolerance: the tolerance parameter to use, the smaller, the closer to the original
        :type tolerance: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.tolerance = tolerance

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "polygon-simplifier"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Simplifies polygons according to the tolerance parameter: the smaller the tolerance, the closer to the original."

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
        parser.add_argument("-t", "--tolerance", type=float, default=0.01, help="The tolerance for the simplification.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.tolerance = ns.tolerance

    def _simplify(self, obj: LocatedObject) -> Tuple[LocatedObject, bool]:
        """
        Simplifies the polygon of the object.

        :param obj: the object to process
        :type obj: LocatedObject
        :return: the potentially updated object
        :rtype: tuple
        """
        result = False

        if obj.has_polygon():
            spoly = locatedobject_polygon_to_shapely(obj)
            spoly_new = simplify(spoly, self.tolerance)
            if isinstance(spoly_new, Polygon) and (len(spoly_new.exterior.coords) < len(spoly.exterior.coords)):
                result = True
                obj = copy.deepcopy(obj)
                x_list, y_list = spoly_new.exterior.coords.xy
                points = []
                for i in range(len(x_list)):
                    points.append(WaiPoint(x=x_list[i], y=y_list[i]))
                obj.set_polygon(WaiPolygon(*points))

        return obj, result

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann = LocatedObjects()
            count = 0
            for obj in item.annotation:
                new_obj, updated = self._simplify(obj)
                ann.append(new_obj)
                if updated:
                    count += 1
            if count > 0:
                item = item.duplicate(annotation=ann)
                self.logger().info("%s: %d polygons updated" % (item.image_name, count))
            result.append(item)

        return flatten_list(result)
