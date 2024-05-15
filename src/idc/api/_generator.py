import abc
import argparse
from typing import List, Dict, Optional

from wai.logging import LOGGING_WARNING
from seppl import Plugin, PluginWithLogging, Initializable, split_cmdline, split_args, args_to_objects


class Generator(PluginWithLogging, Initializable, abc.ABC):
    """
    Base class for generators.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def _check(self) -> Optional[str]:
        """
        Hook method for performing checks.

        :return: None if checks successful, otherwise error message
        :rtype: str
        """
        return None

    def _do_generate(self) -> List[Dict[str, str]]:
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        raise NotImplementedError()

    def generate(self):
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        msg = self._check()
        if msg is not None:
            raise Exception(msg)
        return self._do_generate()

    @classmethod
    def parse_generator(cls, cmdline: str) -> 'Generator':
        """
        Parses the commandline and returns the generator plugin.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :return: the generator plugin
        :rtype: Generator
        """
        result = cls.parse_generators(cmdline)
        if len(result) != 1:
            raise Exception("Expected a single generator, but got: %d" % len(result))
        return result[0]

    @classmethod
    def parse_generators(cls, cmdline: str) -> List['Generator']:
        """
        Parses the commandline and returns the list of generator plugins.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :return: the list of generator plugins
        :rtype: list
        """
        from idc.registry import available_generators
        generator_args = split_args(split_cmdline(cmdline), list(available_generators().keys()))
        return args_to_objects(generator_args, available_generators())


class SingleVariableGenerator(Generator):
    """
    Ancestor for generators that output just a single variable.
    """

    def __init__(self, var_name: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param var_name: the variable name
        :type var_name: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.var_name = var_name

    def _default_var_name(self) -> str:
        """
        Returns the default variable name.

        :return: the default name
        :rtype: str
        """
        raise NotImplementedError()

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-n", "--var_name", type=str, metavar="NAME", default=self._default_var_name(), help="The name of the variable", required=(self._default_var_name() is None))
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.var_name = ns.var_name

    def _check(self) -> Optional[str]:
        """
        Hook method for performing checks.

        :return: None if checks successful, otherwise error message
        :rtype: str
        """
        result = super()._check()

        if self.var_name is None:
            result = "No variable name provided!"

        return result
