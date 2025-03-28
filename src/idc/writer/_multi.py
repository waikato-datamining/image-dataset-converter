import argparse
from typing import List

from wai.logging import LOGGING_WARNING

from seppl import Plugin
from idc.api import ImageData, StreamWriter, DATATYPES, data_type_to_class, BatchWriter, make_list


class MultiWriter(StreamWriter):

    def __init__(self, writers: List[str] = None, data_type: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param writers: the base writers to use (command-line)
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param data_type: the type of output to accept
        :type data_type: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.writers = writers
        self.data_type = data_type
        self._writers = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-multi"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Forwards the incoming data to all the base writers."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-w", "--writer", type=str, default=None, help="The command-line defining the base writer.", required=True, nargs="+")
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to accept", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.writers = ns.writer
        self.data_type = ns.data_type

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

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
        from idc.registry import available_writers
        from seppl import args_to_objects, split_args, split_cmdline

        # split command-line into valid plugin subsets
        valid = available_writers()
        args = split_args(split_cmdline(cmdline), list(valid.keys()))
        return args_to_objects(args, valid, allow_global_options=False)

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.data_type is None:
            raise Exception("No data type defined!")
        if (self.writers is None) or (len(self.writers) == 0):
            raise Exception("No writer(s) defined!")
        self._writers = []
        for writer in self.writers:
            objs = self._parse_commandline(writer)
            if len(objs) == 1:
                _writer = objs[0]
                if self.accepts()[0] in _writer.accepts():
                    self._writers.append(_writer)
                else:
                    raise Exception("Writer '%s' accepts '%s' but '%s' is required!" % (writer, str(_writer.accepts()), str(self.accepts())))
            else:
                raise Exception("Failed to obtain a single writer from command-line: %s" % writer)
        for writer in self._writers:
            writer.initialize()
            writer.session = self.session
        self.logger().info("# writers: %d" % len(self._writers))

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for writer in self._writers:
            if isinstance(writer, StreamWriter):
                writer.write_stream(data)
            elif isinstance(writer, BatchWriter):
                writer.write_batch(make_list(data))
            else:
                raise Exception("Unknown type of writer: %s" % str(type(writer)))

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        if self._writers is not None:
            for writer in self._writers:
                writer.finalize()
