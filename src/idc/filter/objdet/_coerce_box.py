import copy
from typing import List, Tuple

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.common.adams.imaging.locateobjects.constants import KEY_POLY_X, KEY_POLY_Y
from seppl.io import Filter
from idc.api import ObjectDetectionData, flatten_list, make_list


class CoerceBox(Filter):
    """
    Converts all annotation bounds into box regions.
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
        return "coerce-box"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Converts all annotation bounds into box regions."

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

    def _process_annotations(self, ann: LocatedObjects) -> Tuple[LocatedObjects, int]:
        """
        Processes the annotations.

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
            if KEY_POLY_X in obj_new.metadata:
                updated = True
                del obj_new.metadata[KEY_POLY_X]
            if KEY_POLY_Y in obj_new.metadata:
                updated = True
                del obj_new.metadata[KEY_POLY_Y]
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
            ann, updated = self._process_annotations(item.annotation)
            if updated > 0:
                self.logger().info("Updated %d object(s)" % updated)
                item = item.duplicate(annotation=ann)
            result.append(item)

        return flatten_list(result)
