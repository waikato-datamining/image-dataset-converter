import argparse
from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, flatten_list, make_list

DUPLICATE_ACTION_IGNORE = "ignore"
DUPLICATE_ACTION_WARN = "warn"
DUPLICATE_ACTION_DROP = "drop"
DUPLICATE_ACTION_ERROR = "error"
DUPLICATE_ACTIONS = [
    DUPLICATE_ACTION_IGNORE,
    DUPLICATE_ACTION_WARN,
    DUPLICATE_ACTION_DROP,
    DUPLICATE_ACTION_ERROR,
]


class CheckDuplicateFilenames(Filter):
    """
    Ensures that file names are unique (raises an exception if not).
    """

    def __init__(self, action: str = DUPLICATE_ACTION_ERROR,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param action: the action to perform when encountering a duplicate file name
        :type action: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.action = action
        self._names = None
        self._paths = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "check-duplicate-filenames"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Ensures that file names are unique (raises an exception if not)."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

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
        parser.add_argument("-a", "--action", choices=DUPLICATE_ACTIONS, help="The action to perform when encountering a duplicate file name", required=False, default=DUPLICATE_ACTION_ERROR)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.action = ns.action

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._names = set()
        self._paths = dict()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if item.image_name in self._names:
                msg = "File name already encountered: %s" % item.image_name
                if item.source is not None:
                    msg += "\n- full path: %s" % item.source
                if item.image_name in self._paths:
                    msg += "\n- previous file: %s" % self._paths[item.image_name]

                if self.action == DUPLICATE_ACTION_IGNORE:
                    self.logger().debug(msg)
                elif self.action == DUPLICATE_ACTION_WARN:
                    self.logger().warning(msg)
                elif self.action == DUPLICATE_ACTION_DROP:
                    self.logger().warning(msg)
                    self.logger().warning("Dropping file: %s" % item.image_name)
                    item = None
                elif self.action == DUPLICATE_ACTION_ERROR:
                    raise Exception(msg)
                else:
                    raise Exception("Unhandled action: %s" % self.action)

            if item is not None:
                self._names.add(item.image_name)
                if item.source is not None:
                    self._paths[item.image_name] = item.source

        return flatten_list(result)
