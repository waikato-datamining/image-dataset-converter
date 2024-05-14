import argparse
from typing import Optional, List, Dict

from wai.logging import LOGGING_WARNING
from idc.api import SingleVariableGenerator


class ListGenerator(SingleVariableGenerator):
    """
    Outputs the list of provided values.
    """

    def __init__(self, values: List[str] = None, var_name: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param values: the starting value
        :type values: list
        :param var_name: the variable name
        :type var_name: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(var_name=var_name, logger_name=logger_name, logging_level=logging_level)
        self.values = values

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "list"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Outputs the specified values."

    def _default_var_name(self) -> str:
        """
        Returns the default variable name.

        :return: the default name
        :rtype: str
        """
        return "v"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-v", "--values", type=str, metavar="VALUE", default=None, help="The list of values to use.", nargs="+")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.values = ns.values

    def _check(self) -> Optional[str]:
        """
        Hook method for performing checks.

        :return: None if checks successful, otherwise error message
        :rtype: str
        """
        result = super()._check()

        if result is None:
            if (self.values is None) or (len(self.values) == 0):
                result = "No values provided!"

        return result

    def _do_generate(self) -> List[Dict[str, str]]:
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        result = []
        for value in self.values:
            result.append({self.var_name: str(value)})
        return result
