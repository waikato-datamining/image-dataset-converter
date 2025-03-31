import argparse
from typing import List, Iterable

from seppl import Plugin
from wai.logging import LOGGING_WARNING

from idc.api import DATATYPES, data_type_to_class, ImageData
from idc.api import Reader

READ_ORDER_SEQUENTIAL = "sequential"
READ_ORDER_INTERLEAVED = "interleaved"
READ_ORDERS = [
    READ_ORDER_SEQUENTIAL,
    READ_ORDER_INTERLEAVED,
]


class MultiReader(Reader):

    def __init__(self, readers: List[str] = None, read_order: str = None, data_type: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param readers: the list of base readers to use (command-lines)
        :param read_order: how the base readers are being used
        :type read_order: str
        :param data_type: the type of output to generate from the images
        :type data_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.readers = readers
        self.read_order = read_order
        self.data_type = data_type
        self._readers = None
        self._finalize = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-multi"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Reads data using the specified base readers and combines their output."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-r", "--reader", type=str, default=None, help="The command-line defining the base reader.", required=True, nargs="+")
        parser.add_argument("-o", "--read_order", choices=READ_ORDERS, type=str, default=READ_ORDER_SEQUENTIAL, help="How to use the output from the readers.", required=False)
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.readers = ns.reader
        self.read_order = ns.read_order
        self.data_type = ns.data_type

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.data_type is None:
            return [ImageData]
        else:
            return [data_type_to_class(self.data_type)]

    def _parse_commandline(self, cmdline: str) -> List[Plugin]:
        """
        Parses the command-line and returns the list of plugins it represents.
        Raises an exception in case of an invalid sub-flow.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :return:
        """
        from idc.registry import available_readers
        from seppl import args_to_objects, split_args, split_cmdline

        # split command-line into valid plugin subsets
        valid = available_readers()
        args = split_args(split_cmdline(cmdline), list(valid.keys()))
        return args_to_objects(args, valid, allow_global_options=False)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.data_type is None:
            raise Exception("No data type defined!")
        if (self.readers is None) or (len(self.readers) == 0):
            raise Exception("No reader(s) defined!")
        if self.read_order is None:
            self.read_order = READ_ORDER_SEQUENTIAL
        if self.read_order not in READ_ORDERS:
            raise Exception("Unknown read order: %s" % self.read_order)
        self._readers = []
        for reader in self.readers:
            objs = self._parse_commandline(reader)
            if len(objs) == 1:
                _reader = objs[0]
                if _reader.generates() == self.generates():
                    self._readers.append(_reader)
                else:
                    raise Exception("Reader '%s' generates '%s' but '%s' is required!" % (reader, str(_reader.generates()), str(self.generates())))
            else:
                raise Exception("Failed to obtain a single reader from command-line: %s" % reader)
        for reader in self._readers:
            reader.initialize()
            reader.session = self.session
        self.logger().info("# readers: %d" % len(self._readers))
        self._finalize = []

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        if self.read_order == READ_ORDER_SEQUENTIAL:
            readers = self._readers[:]
            for reader in readers:
                while not reader.has_finished():
                    for data in reader.read():
                        yield data
                self._finalize.append(self._readers.pop(0))
        elif self.read_order == READ_ORDER_INTERLEAVED:
            while len(self._readers) > 0:
                for reader in self._readers:
                    if not reader.has_finished():
                        for data in reader.read():
                            yield data
                    if reader.has_finished():
                        self._readers.remove(reader)
                        self._finalize.append(reader)
        else:
            raise Exception("Unhandled read order: %s" % self.read_order)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._readers) == 0

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        if self._finalize is not None:
            for reader in self._finalize:
                reader.finalize()
