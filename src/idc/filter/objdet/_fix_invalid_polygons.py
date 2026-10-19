import copy
from typing import List, Tuple

from shapely import make_valid
from shapely.validation import explain_validity
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, locatedobject_polygon_to_shapely, shapely_to_locatedobject
from kasperl.api import make_list, flatten_list
from seppl.io import BatchFilter
from ._check_polygon_validity import VALID_GEOMETRY


class FixInvalidPolygons(BatchFilter):
    """
    Tries to fix invalid polygons.
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
        return "fix-invalid-polygons"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Tries to fix invalid polygons."

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

    def _process_annotations(self, image_name: str, ann: LocatedObjects) -> Tuple[LocatedObjects, int]:
        """
        Processes the annotations.

        :param image_name: the name of the current image (for logging only)
        :type image_name: str
        :param ann: the annotations to process
        :type ann: LocatedObjects
        :return: the tuple of processed annotations and how many were updated
        :rtype: tuple
        """
        if isinstance(ann, LocatedObjects):
            ann_new = LocatedObjects()
        else:
            ann_new = NormalizedLocatedObjects()
        count = 0

        for obj in ann:
            obj_new = copy.deepcopy(obj)
            updated = False
            if obj_new.has_polygon():
                poly = locatedobject_polygon_to_shapely(obj_new)
                validity = explain_validity(poly)
                if validity != VALID_GEOMETRY:
                    poly = make_valid(geometry=poly)
                    obj_updated = shapely_to_locatedobject(poly)
                    if obj_updated.has_polygon():
                        obj_new.set_polygon(obj_updated.get_polygon())
                        updated = True
                    else:
                        self.logger().warning("Failed to fix polygon: %s/%s" % (image_name, str(obj)))
            if updated:
                count += 1
            ann_new.append(obj_new)

        return ann_new, count

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann, updated = self._process_annotations(item.image_name, item.annotation)
            if updated > 0:
                self.logger().info("Updated %d polygon(s)" % updated)
                item = item.duplicate(annotation=ann)
            result.append(item)

        return flatten_list(result)
