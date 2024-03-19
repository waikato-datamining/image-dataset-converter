import argparse
from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import flatten_list, make_list


class MaxRecords(Filter):
    """
    Suppresses records after the specified maximum number of records have passed through.
    """

    def __init__(self, max_records: int = -1, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param max_records: the maximum number of records to process <= 0 is unlimited
        :type max_records: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.max_records = max_records
        self._counter = 0

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "max-records"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Suppresses records after the specified maximum number of records have passed through."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--max_records", type=int, help="The maximum number number of records to let through before suppressing records.", default=-1, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.max_records = ns.max_records

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._counter = 0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            # maximum reached?
            if (self.max_records > 0) and (self._counter >= self.max_records):
                if self._counter == self.max_records:
                    self.logger().info("Maximum # of records reached: %d" % self.max_records)
                item = None

            self._counter += 1

            if item is not None:
                result.append(item)

        return flatten_list(result)
