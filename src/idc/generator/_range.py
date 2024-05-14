import argparse
from typing import Optional, List, Dict

from wai.logging import LOGGING_WARNING
from idc.api import SingleVariableGenerator


class RangeGenerator(SingleVariableGenerator):
    """
    Generates a range of integers.
    """

    def __init__(self, from_: int = None, to: int = None, step: int = None, var_name: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param from_: the starting value
        :type from_: int
        :param to: the end value (excluded)
        :type to: int
        :param step: the step between values
        :type step: int
        :param var_name: the variable name
        :type var_name: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(var_name=var_name, logger_name=logger_name, logging_level=logging_level)
        self.from_ = from_
        self.to = to
        self.step = step

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "range"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Iterates over a range of values."

    def _default_var_name(self) -> str:
        """
        Returns the default variable name.

        :return: the default name
        :rtype: str
        """
        return "i"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--from", type=int, metavar="START", default=None, help="The starting value", required=True)
        parser.add_argument("-t", "--to", type=int, metavar="END", default=None, help="The end value (excluded)", required=True)
        parser.add_argument("-s", "--step", type=int, metavar="STEP", default=1, help="The increment between values", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.from_ = getattr(ns, "from")
        self.to = ns.to
        self.step = ns.step

    def _check(self) -> Optional[str]:
        """
        Hook method for performing checks.

        :return: None if checks successful, otherwise error message
        :rtype: str
        """
        result = super()._check()

        if self.step is None:
            self.step = 1

        if result is None:
            if self.from_ is None:
                result = "No FROM value provided!"
            elif self.to is None:
                result = "No TO value provided!"
            elif self.step == 0:
                result = "STEP cannot be 0!"
            elif self.step > 0:
                if self.from_ >= self.to:
                    result = "FROM must be smaller than TO (f=%s, t=%s, s=%s)!" % (str(self.from_), str(self.to), str(self.step))
            else:
                if self.from_ <= self.to:
                    result = "FROM must be less than TO (f=%s, t=%s, s=%s)!" % (str(self.from_), str(self.to), str(self.step))

        return result

    def _do_generate(self) -> List[Dict[str, str]]:
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        result = []
        for i in range(self.from_, self.to, self.step):
            result.append({self.var_name: str(i)})
        return result
