import argparse
from typing import List

from seppl.io import Filter, FILTER_ACTIONS, FILTER_ACTION_DISCARD, FILTER_ACTION_KEEP
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, make_list, flatten_list, \
    COMPARISONS_EXT, COMPARISON_EQUAL, COMPARISON_CONTAINS, COMPARISON_MATCHES, COMPARISON_EXT_HELP, \
    compare_values


class MetaDataObjectDetection(Filter):
    """
    Keeps or discards data records based on meta-data values.
    """

    def __init__(self, field: str = None, action: str = FILTER_ACTION_KEEP,
                 comparison: str = COMPARISON_EQUAL, value=None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param field: the name of the meta-data field to perform the comparison on
        :type field: str
        :param action: the action to perform
        :type action: str
        :param comparison: the comparison to perform
        :type comparison: str
        :param value: the value to compare with
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

        if action not in FILTER_ACTIONS:
            raise Exception("Invalid action: %s" % action)
        if comparison not in COMPARISONS_EXT:
            raise Exception("Invalid comparison: %s" % comparison)

        self.field = field
        self.value = value
        self.comparison = comparison
        self.action = action
        self.kept = 0
        self.discarded = 0

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "metadata-od"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Keeps or discards object detection annotations based on meta-data comparisons. " \
               + "Performs the following comparison: METADATA_VALUE COMPARISON VALUE. " \
               + "Annotations that do not have the required field get discarded automatically."

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
        parser.add_argument("-f", "--field", type=str, help="The meta-data field to use in the comparison", required=True)
        parser.add_argument("-v", "--value", type=str, help="The value to use in the comparison", required=True)
        parser.add_argument("-c", "--comparison", choices=COMPARISONS_EXT, default=COMPARISON_EQUAL, help="How to compare the value with the meta-data value; " + COMPARISON_EXT_HELP
                            + "; in case of '" + COMPARISON_CONTAINS + "' and '" + COMPARISON_MATCHES + "' the supplied value represents the substring to find/regexp to search with")
        parser.add_argument("-a", "--action", choices=FILTER_ACTIONS, default=FILTER_ACTION_KEEP, help="How to react when a keyword is encountered")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.field = ns.field
        self.value = ns.value
        self.comparison = ns.comparison
        self.action = ns.action

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.field is None:
            raise Exception("No meta-data field provided!")
        if self.value is None:
            raise Exception("No value provided to compare with!")
        self.kept = 0
        self.discarded = 0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if not isinstance(item, ObjectDetectionData):
                raise Exception("Unhandled type of data: %s" % str(type(item)))

            lobjs = []
            for lobj in item.annotation:
                lobj_result = lobj
                meta = lobj.metadata
                # no meta-data -> reject
                if meta is None:
                    self.logger().info("No meta-data, discarded")
                    self.discarded += 1
                    continue

                # key not present -> reject
                if self.field not in meta:
                    self.logger().info("Field '%s' not meta-data, discarded" % self.field)
                    self.discarded += 1
                    continue

                v1 = meta[self.field]
                v2 = self.value
                comp_result = compare_values(v1, self.comparison, v2)

                if self.action == FILTER_ACTION_KEEP:
                    if not comp_result:
                        lobj_result = None
                elif self.action == FILTER_ACTION_DISCARD:
                    if comp_result:
                        lobj_result = None
                else:
                    raise Exception("Unhandled action: %s" % self.action)

                if lobj_result is None:
                    self.discarded += 1
                else:
                    lobjs.append(lobj_result.get_clone())
                    self.kept += 1

                info = "keeping" if (lobj_result is not None) else "discarding"
                comp = str(meta[self.field]) + " " + self.comparison + " " + str(self.value) + " = " + str(comp_result)
                self.logger().debug("Field '%s': '%s' --> %s" % (self.field, comp, info))

            item_new = item.duplicate(annotation=LocatedObjects(lobjs))
            result.append(item_new)
            change = len(item.annotation) - len(item_new.annotation)
            if change > 0:
                self.logger().info("# annotations removed: %d" % change)
                self.logger().info("# annotations left: %d" % len(item_new.annotation))

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.logger().info("# kept: %d" % self.kept)
        self.logger().info("# discarded: %d" % self.discarded)
