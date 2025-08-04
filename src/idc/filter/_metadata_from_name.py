import argparse
import copy
import re
from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import make_list, flatten_list


SOURCE_NAME = "name"
SOURCE_PATH = "path"
SOURCES = [
    SOURCE_NAME,
    SOURCE_PATH,
]


class MetaDataFromName(Filter):
    """
    Extracts a sub-string from the image name or path and stores it in the meta-data.
    """

    def __init__(self, source: str = None, regexp: str = None, metadata_key: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param source: where to apply the regexp to, default is name
        :type source: str
        :param regexp: the regular expression to apply to the name (1st group gets used as label)
        :type regexp: str
        :param metadata_key: the metadata key to store the extracted substring under
        :type metadata_key: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.regexp = regexp
        self.metadata_key = metadata_key

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "metadata-from-name"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Extracts a sub-string from the image name or path and stores it in the meta-data."

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
        parser.add_argument("-s", "--source", choices=SOURCES, help="The string to apply the regular expression to for extracting the meta-data.", default=SOURCE_NAME, required=False)
        parser.add_argument("-r", "--regexp", type=str, help="The regular expression apply to the image name, with the 1st group being used as the meta-data value.", default=None, required=False)
        parser.add_argument("-k", "--metadata_key", type=str, help="The key in the meta-data to store the extracted sub-string under.", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.source
        self.regexp = ns.regexp
        self.metadata_key = ns.metadata_key

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.source is None:
            self.source = SOURCE_NAME
        if self.metadata_key is None:
            raise Exception("No meta-data key provided!")

    def _update(self, data):
        """
        Updates the label of the record.

        :param data: the record to update
        """
        try:
            # get string for regexp
            if self.source == SOURCE_NAME:
                source = data.image_name
            elif self.source == SOURCE_PATH:
                source = data.source
            else:
                raise Exception("Unhandled source: %s" % self.source)
            if source is None:
                self.logger().warning("No %s available to apply regexp to: %s" % (self.source, str(data)))
                return data

            # apply regexp
            m = re.search(self.regexp, source)
            if m is None:
                return data
            value = m.group(1)

            # set meta-data
            result = copy.deepcopy(data)
            if not result.has_metadata():
                meta = dict()
            else:
                meta = result.get_metadata()
            meta[self.metadata_key] = value
            self.logger().info("%s = %s" % (self.metadata_key, value))
            result.set_metadata(meta)
            return result
        except:
            self.logger().exception("Failed to extract meta-data value from: %s" % str(data))
            return data

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            result.append(self._update(item))

        return flatten_list(result)
