import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from seppl import Initializable
import seppl.io


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

    def __init__(self, split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
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
        self.split_group = None
        self.splitter = None
        seppl.io.init_splitting_params(self, split_names=split_names, split_ratios=split_ratios)

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        seppl.io.add_splitting_params(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        seppl.io.transfer_splitting_params(ns, self)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        seppl.io.initialize_splitting(self)


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

    def __init__(self, split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param split_group: the regular expression with a single group used for keeping items in the same split, e.g., for identifying the base name of a file or the sample ID
        :type split_group: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        # define the members
        self.split_names = None
        self.split_ratios = None
        self.split_group = None
        self.splitter = None
        # initialize the members
        seppl.io.init_splitting_params(self, split_names=split_names, split_ratios=split_ratios, split_group=split_group)

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        seppl.io.add_splitting_params(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        seppl.io.transfer_splitting_params(ns, self)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        seppl.io.initialize_splitting(self)


def parse_writer(writer: str) -> seppl.io.Writer:
    """
    Parses the command-line and instantiates the writer.

    :param writer: the command-line to parse
    :type writer: str
    :return: the writer
    :rtype: seppl.io.Writer
    """
    from seppl import split_args, split_cmdline, args_to_objects
    from idc.registry import available_writers

    if writer is None:
        raise Exception("No writer command-line supplied!")
    valid = dict()
    valid.update(available_writers())
    args = split_args(split_cmdline(writer), list(valid.keys()))
    objs = args_to_objects(args, valid, allow_global_options=False)
    if len(objs) == 1:
        if isinstance(objs[0], seppl.io.Writer):
            result = objs[0]
        else:
            raise Exception("Expected instance of Writer but got: %s" % str(type(objs[0])))
    else:
        raise Exception("Expected to obtain one writer from '%s' but got %d instead!" % (writer, len(objs)))
    return result


def add_annotations_only_param(parser: argparse.ArgumentParser):
    """
    Adds the --annotations_only parameter to the parser, as used by writers of type AnnotationOnlyWriter.

    :param parser: the parser
    :type parser: argparse.ArgumentParser
    """
    parser.add_argument("--annotations_only", action="store_true", help="Outputs only the annotations and skips the base image.")


class AnnotationsOnlyWriter:
    """
    Mixin for writers that can output the annotations by itself.
    """
    pass
