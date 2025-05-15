import argparse
from typing import List

from seppl import AliasSupporter
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import DepthData, depth_to_grayscale, DATATYPES, data_type_to_class, DataTypeSupporter, flatten_list, \
    make_list, safe_deepcopy


class DepthToGrayscale(Filter, AliasSupporter, DataTypeSupporter):
    """
    Turns the depth information into a grayscale image.
    """

    def __init__(self, min_value: float = None, max_value: float = None, data_type: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param min_value: the minimum value to use (smaller values get set to this), ignored if None
        :type min_value: float
        :param max_value: the maximum value to use (larger values get set to this), ignored if None
        :type max_value: float
        :param data_type: the type of output to generate from the images
        :type data_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.min_value = min_value
        self.max_value = max_value
        self.data_type = data_type
        self._output_cls = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "depth-to-grayscale"

    def aliases(self) -> List[str]:
        """
        Returns the aliases under which the plugin is known under/available as well.

        :return: the aliases
        :rtype: list
        """
        return ["depth-to-greyscale"]

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Turns the depth information into a grayscale image."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [DepthData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.data_type is None:
            return [DepthData]
        else:
            return [data_type_to_class(self.data_type)]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--min_value", type=float, help="The minimum value to use, smaller values get set to this.", default=None, required=False)
        parser.add_argument("-M", "--max_value", type=float, help="The maximum value to use, larger values get set to this.", default=None, required=False)
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.min_value = ns.min_value
        self.max_value = ns.max_value
        self.data_type = ns.data_type

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.min_value is not None) and (self.max_value is not None):
            if self.min_value >= self.max_value:
                raise Exception("The min value must be smaller than the max value, but got: min=%f, max=%f" % (self.min_value, self.max_value))
        self._output_cls = data_type_to_class(self.data_type)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            img = depth_to_grayscale(item.annotation, min_value=self.min_value, max_value=self.max_value, logger=self.logger())
            new_item = self._output_cls(image_name=item.image_name, image_format=item.image_format, image=img,
                                        metadata=safe_deepcopy(item.get_metadata()))
            result.append(new_item)

        return flatten_list(result)
