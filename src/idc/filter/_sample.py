import argparse
from random import Random
from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import flatten_list, make_list


class Sample(Filter):
    """
    Selects a sub-sample from the stream.
    """

    def __init__(self, seed: int = None, threshold: float = 0.0,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param seed: the seed value to use for the random number generator; randomly seeded if not provided
        :type seed: int
        :param threshold: the threshold to use for Random.rand(): if equal or above, sample gets selected; range: 0-1; default: 0 (= always)
        :type threshold: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.seed = seed
        self.threshold = threshold
        self._random = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "sample"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Selects a sub-sample from the stream."

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
        parser.add_argument("-s", "--seed", type=int, help="The seed value to use for the random number generator; randomly seeded if not provided.", default=None, required=False)
        parser.add_argument("-T", "--threshold", type=float, help="The threshold to use for Random.rand(): if equal or above, sample gets selected; range: 0-1; 0 = always.", default=0.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.seed = ns.seed
        self.threshold = ns.threshold

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._random = Random(self.seed)
        threshold = 0.0 if self.threshold is None else self.threshold
        if (threshold < 0) or (threshold > 1):
            raise Exception("Threshold must satisfy x >= 0 and x <= 1, supplied: %f" % threshold)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            threshold = 0.0 if self.threshold is None else self.threshold
            if self._random.random() >= threshold:
                result.append(item)

        return flatten_list(result)
