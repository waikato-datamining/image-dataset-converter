import argparse
from typing import List

from wai.logging import LOGGING_WARNING

from idc.api import DATATYPES, data_type_to_class, ImageData, SplittableStreamWriter, make_list, load_function


class PythonFunctionWriter(SplittableStreamWriter):

    def __init__(self, function: str = None, data_type: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param function: the function to use (module_name:function_name)
        :type function: str
        :param data_type: the type of output to generate from the images
        :type data_type: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, logger_name=logger_name, logging_level=logging_level)
        self.function = function
        self.data_type = data_type
        self._input_cls = None
        self._function = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-pyfunc"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Processes the images of the specified data type via the declared Python function. The function must take an image container as input (matching the data type class) and an optional 'split' string parameter."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--function", type=str, default=None, help="The Python function to use, format: module_name:function_name", required=True)
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.function = ns.function
        self.data_type = ns.data_type

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._input_cls = data_type_to_class(self.data_type)
        self._function = load_function(self.function)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            if issubclass(type(item), self._input_cls):
                split = None
                if self.splitter is not None:
                    split = self.splitter.next()
                self.logger().info("Processing image '%s' (split: %s)" % (item.image_name, str(split)))
                self._function(item, split)
            else:
                self.logger().error("Did not receive an object of type '%s' but of type '%s'!" % (self._input_cls, type(item)))
