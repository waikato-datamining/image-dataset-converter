import argparse
import copy
import re

from typing import List

from wai.logging import LOGGING_WARNING
from seppl.io import Filter
from idc.api import ImageClassificationData


class LabelFromName(Filter):
    """
    Extracts the classification label from the image name.
    """

    def __init__(self, regexp: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param regexp: the regular expression to apply to the name (1st group gets used as label)
        :type regexp: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.regexp = regexp

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "label-from-name"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Extracts the classification label from the image name."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-r", "--regexp", type=str, help="The regular expression apply to the image name, with the 1st group being used as the label.", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.regexp = ns.regexp

    def _update(self, data):
        """
        Updates the label of the record.

        :param data: the record to update
        """
        try:
            name = data.image_name
            if name is None:
                self.logger().warning("No image name available: %s" % str(data))
                return data
            m = re.search(self.regexp, name)
            if m is None:
                return data
            label = m.group(1)
            result = copy.deepcopy(data)
            result.annotation = label
            return result
        except:
            self.logger().exception("Failed to extract label from: %s" % data.image_name)
            return data

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        if isinstance(data, list):
            result = list(data)
            for i, item in enumerate(data):
                result[i] = self._update(item)
        else:
            result = self._update(data)

        return result
