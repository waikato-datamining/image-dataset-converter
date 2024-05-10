import argparse
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import flatten_list, make_list, ImageData, DATATYPES, data_type_to_class, load_function


class PythonFunctionFilter(Filter):
    """
    Selects a sub-sample from the stream.
    """

    def __init__(self, function: str = None, input_data_type: str = None, output_data_type: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param function: the function to use (module_name:function_name)
        :type function: str
        :param input_data_type: the type of output to generate from the images
        :type input_data_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.function = function
        self.input_data_type = input_data_type
        self.output_data_type = output_data_type
        self._input_cls = None
        self._output_cls = None
        self._function = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "pyfunc-filter"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "The declared Python function processes image containers of the specified input type and generates ones of the specified output type. The function must handle a single image container or an iterable of image containers and return a single image container or an iterable of image containers."

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
        return [ImageData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input_data_type", choices=DATATYPES, type=str, default=None, help="The type of data to receive", required=True)
        parser.add_argument("-f", "--function", type=str, default=None, help="The Python function to use, format: module_name:function_name", required=True)
        parser.add_argument("-o", "--output_data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.input_data_type = ns.input_data_type
        self.function = ns.function
        self.output_data_type = ns.output_data_type

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._input_cls = data_type_to_class(self.input_data_type)
        self._function = load_function(self.function)
        self._output_cls = data_type_to_class(self.output_data_type)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if issubclass(type(item), self._input_cls):
                new_items = self._function(item)
                if new_items is None:
                    continue
                new_items = make_list(new_items)
                for new_item in new_items:
                    if new_item is None:
                        continue
                    if issubclass(type(item), self._output_cls):
                        result.append(new_item)
                    else:
                        self.logger().error("Function '%s' did not return an object of type '%s' but of type '%s'!" % (self.function, self._output_cls, type(item)))
            else:
                self.logger().error("Did not receive an object of type '%s' but of type '%s'!" % (self._input_cls, type(item)))

        return flatten_list(result)
