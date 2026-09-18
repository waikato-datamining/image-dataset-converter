import argparse
import logging
from typing import List

from shapely.validation import explain_validity
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, locatedobject_polygon_to_shapely
from kasperl.api import make_list, flatten_list, safe_deepcopy
from seppl.io import BatchFilter

ACTION_RECORD_ALL = "record-all"
ACTION_RECORD_VALID = "record-valid"
ACTION_RECORD_INVALID = "record-invalid"
ACTIONS = [
    ACTION_RECORD_ALL,
    ACTION_RECORD_INVALID,
    ACTION_RECORD_VALID,
]

VALID_GEOMETRY = "Valid Geometry"

DEFAULT_POLYGON_VALIDITY_FIELD = "polygon_validity"


class CheckPolygonValidity(BatchFilter):
    """
    Transfers the image dimensions to the meta-data.
    """

    def __init__(self, action: str = None, field: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param action: the action to perform
        :type action: str
        :param field: the object's meta-data field to use for storing the validity result
        :type field: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.action = action
        self.field = field

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "check-polygon-validity"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Checks whether the polygons of object annotations are valid and stores the result in the object's meta-data."

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
        parser.add_argument("-a", "--action", choices=ACTIONS, default=ACTION_RECORD_ALL, help="The action to perform when analyzing the validity of polygons.", required=False)
        parser.add_argument("-f", "--field", metavar="FIELD", type=str, default=DEFAULT_POLYGON_VALIDITY_FIELD, help="The object's metadata field for the result of the validity test.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.action = ns.action
        self.field = ns.field

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.action is None:
            self.action = ACTION_RECORD_ALL
        if self.action not in ACTIONS:
            raise Exception("Unsupported action: %s" % self.action)
        if (self.field is None) or (len(self.field.strip()) == 0):
            self.field = DEFAULT_POLYGON_VALIDITY_FIELD

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if isinstance(item, ObjectDetectionData):
                item_new = item
                if item.has_annotation():
                    ann_new = LocatedObjects()
                    modified = False
                    for lobj in item.annotation:
                        lobj = safe_deepcopy(lobj)
                        if not lobj.has_polygon():
                            ann_new.append(lobj)
                            continue
                        poly = locatedobject_polygon_to_shapely(lobj)
                        validity = explain_validity(poly)
                        if self.logger().isEnabledFor(logging.INFO):
                            self.logger().info("%s: %s" % (str(lobj), validity))
                        if self.action == ACTION_RECORD_ALL:
                            modified = True
                            lobj.metadata[self.field] = validity
                            ann_new.append(lobj)
                        elif self.action == ACTION_RECORD_INVALID:
                            if validity != VALID_GEOMETRY:
                                modified = True
                                lobj.metadata[self.field] = validity
                                ann_new.append(lobj)
                        elif self.action == ACTION_RECORD_VALID:
                            if validity == VALID_GEOMETRY:
                                modified = True
                                lobj.metadata[self.field] = validity
                                ann_new.append(lobj)
                    if modified:
                        item_new = item.duplicate()
                        item_new.annotation = ann_new

                result.append(item_new)
            else:
                self.logger().warning("Cannot process data type: %s" % str(type(item)))

        return flatten_list(result)
