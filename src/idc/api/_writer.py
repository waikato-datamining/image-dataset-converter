import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from seppl import Initializable
import seppl.io
from ._splitting import init_splitting_params, add_splitting_params, transfer_splitting_params, initialize_splitting


class BatchWriter(seppl.io.BatchWriter, Initializable):
    """
    Ancestor for dataset batch writers.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)


class SplittableBatchWriter(BatchWriter):
    """
    Ancestor for dataset batch writers.
    """

    def __init__(self, split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.split_names = None
        self.split_ratios = None
        self.splitter = None
        init_splitting_params(self, split_names=split_names, split_ratios=split_ratios)

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        add_splitting_params(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        transfer_splitting_params(ns, self)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        initialize_splitting(self)


class StreamWriter(seppl.io.StreamWriter, Initializable):
    """
    Ancestor for dataset stream writers.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)


class SplittableStreamWriter(StreamWriter):
    """
    Ancestor for dataset stream writers.
    """

    def __init__(self, split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.split_names = None
        self.split_ratios = None
        self.splitter = None
        init_splitting_params(self, split_names=split_names, split_ratios=split_ratios)

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        add_splitting_params(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        transfer_splitting_params(ns, self)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        initialize_splitting(self)
