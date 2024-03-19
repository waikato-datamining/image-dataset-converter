import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from seppl import MetaDataHandler, get_metadata, AnyData
from seppl.io import Splitter, Filter
from idc.api import flatten_list, make_list

META_SPLIT = "split"
""" the key for storing the split name in the meta-data. """


class Split(Filter):
    """
    Splits the incoming records into the specified split ratios by setting the 'split' meta-data value. Also stores the split names in the current session.
    """

    def __init__(self, split_ratios: List[int] = None, split_names: List[str] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param split_ratios: the ratios for splitting the data (must some up to 100)
        :type split_ratios: list
        :param split_names: the names for the splits (will be stored in the meta-data)
        :type split_names: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.split_ratios = split_ratios
        self.split_names = split_names
        self._splitter = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "split"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Splits the incoming records into the specified split ratios by setting the '%s' meta-data value. Also stores the split names in the current session." % META_SPLIT

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
        parser.add_argument("-r", "--split_ratios", type=int, default=None, help="The split ratios to use for generating the splits (must sum up to 100)", nargs="+")
        parser.add_argument("-n", "--split_names", type=str, default=None, help="The split names to use for the generated splits, get stored in the meta-data under the key '" + META_SPLIT + "'.", nargs="+")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.split_ratios = ns.split_ratios[:]
        self.split_names = ns.split_names[:]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        self._splitter = Splitter(self.split_ratios, self.split_names)
        self._splitter.initialize()

    def _output_stats(self):
        """
        Outputs the statistics.
        """
        stats = self._splitter.stats()
        for split in stats:
            self.logger().info("%s: %d" % (split, stats[split]))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        if self._has_input_changed(update=True):
            if self._splitter.counter() > 0:
                self.logger().info("Input changed, resetting splitter.")
                self._output_stats()
                self._splitter.reset()

        result = []
        for item in make_list(data):
            # get meta data
            meta = get_metadata(item)
            if meta is None:
                if not isinstance(item, MetaDataHandler):
                    raise Exception("Cannot access meta-data for type: %s" % str(type(item)))
                else:
                    meta = dict()
                    item.set_metadata(meta)

            # find split according to schedule
            meta[META_SPLIT] = self._splitter.next()
            result.append(item)

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self._output_stats()
