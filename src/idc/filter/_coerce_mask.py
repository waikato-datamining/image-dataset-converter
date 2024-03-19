import copy
from typing import List, Tuple, Union

from wai.logging import LOGGING_WARNING
from wai.common.geometry import Polygon, Point, NormalizedPolygon, NormalizedPoint
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from seppl.io import Filter
from idc.api import ObjectDetectionData, flatten_list, make_list


class CoerceMask(Filter):
    """
    Coerces the bounds of the annotations to all be polygon-masks.
    Annotations which already have polygons keep theirs, but those
    without are given a rectangular polygon in the shape of their
    bounding box.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "coerce-mask"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Coerces the bounds of the annotations to all be polygon-masks. " \
               "Annotations which already have polygons keep theirs, but those " \
               "without are given a rectangular polygon in the shape of their bounding box."

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

    def _process_annotations(self, ann: Union[LocatedObjects, NormalizedLocatedObjects]) -> Tuple[Union[LocatedObjects, NormalizedLocatedObjects], int]:
        """
        Processes the annotations.

        :param ann: the annotations to process
        :type ann: LocatedObjects
        :return: the tuple of processed annotations and how many were updated
        :rtype: tuple
        """
        normalized = isinstance(ann, NormalizedLocatedObjects)
        if normalized:
            ann_new = LocatedObjects()
        else:
            ann_new = NormalizedLocatedObjects()
        updated = 0

        for obj in ann:
            obj_new = copy.deepcopy(obj)
            if not obj_new.has_polygon():
                updated += 1
                if normalized:
                    points = [Point(obj_new.x, obj_new.y),
                              Point(obj_new.x + obj_new.width - 1, obj_new.y),
                              Point(obj_new.x + obj_new.width - 1, obj_new.y + obj_new.height - 1),
                              Point(obj_new.x, obj_new.y + obj_new.height - 1)]
                    poly = Polygon(*points)
                else:
                    points = [NormalizedPoint(obj_new.x, obj_new.y),
                              NormalizedPoint(obj_new.x + obj_new.width, obj_new.y),
                              NormalizedPoint(obj_new.x + obj_new.width, obj_new.y + obj_new.height),
                              NormalizedPoint(obj_new.x, obj_new.y + obj_new.height)]
                    poly = NormalizedPolygon(*points)
                obj_new.set_polygon(poly)
            ann_new.append(obj_new)

        return ann_new, updated

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann, updated = self._process_annotations(item.annotation)
            if updated > 0:
                self.logger().info("Updated %d object(s)" % updated)
                item = item.duplicate(annotation=ann)
            result.append(item)

        return flatten_list(result)
