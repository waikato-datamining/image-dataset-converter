import argparse
import glob
import os
from time import sleep
from typing import List, Iterable

from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl import Initializable, init_initializable
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, Reader, parse_reader

GLOB_NAME_PLACEHOLDER = "{NAME}"
""" The glob placeholder for identifying other input files. """


class PollDir(Reader, PlaceholderSupporter):

    def __init__(self, dir_in: str = None, dir_out: str = None, poll_wait: float = None, process_wait: float = None,
                 delete_input: bool = False, extensions: List[str] = None,
                 other_input_files: List[str] = None, max_files: int = None, base_reader: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param dir_in: the directory to poll for new files
        :type dir_in: str
        :param dir_out: the directory to move the files to before presenting them to the base reader
        :type dir_out: str
        :param poll_wait: the seconds to wait between polls
        :type poll_wait: float
        :param process_wait: the seconds to wait before processing the files (e.g., to be fully written to disk)
        :type process_wait: float
        :param delete_input: whether to delete the input data
        :type delete_input: bool
        :param extensions: the list of extensions to poll the directory for
        :type extensions: list
        :param other_input_files: other files that need to be present, glob expression (use placeholder GLOB_NAME_PLACEHOLDER)
        :type other_input_files: list
        :param max_files: the maximum number of files to poll (<1 for no limit)
        :type max_files: int
        :param base_reader: the base reader to use (command-line)
        :type base_reader: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.dir_in = dir_in
        self.dir_out = dir_out
        self.poll_wait = poll_wait
        self.process_wait = process_wait
        self.delete_input = delete_input
        self.extensions = extensions
        self.other_input_files = other_input_files
        self.max_files = max_files
        self.base_reader = base_reader
        self._inputs = None
        self._current_input = None
        self._base_reader = None
        self._actual_dir_in = None
        self._actual_dir_out = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "poll-dir"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Polls a directory for files and presents them to the base reader."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--dir_in", type=str, help="The directory to poll; " + placeholder_list(obj=self), required=True)
        parser.add_argument("-o", "--dir_out", type=str, help="The directory to move the files to; " + placeholder_list(obj=self), required=True)
        parser.add_argument("-w", "--poll_wait", type=float, help="The poll interval in seconds", required=False, default=1.0)
        parser.add_argument("-W", "--process_wait", type=float, help="The number of seconds to wait before processing the polled files (e.g., waiting for files to be fully written)", required=False, default=0.0)
        parser.add_argument("-d", "--delete_input", action="store_true", help="Whether to delete the input files rather than move them to --dir_out directory", required=False, default=False)
        parser.add_argument("-e", "--extensions", type=str, help="The extensions of the files to poll (incl. dot)", required=True, nargs="+")
        parser.add_argument("-O", "--other_input_files", type=str, help="The glob expression(s) for capturing other files apart from the input files; use " + GLOB_NAME_PLACEHOLDER + " in the glob expression for the current name", required=False, default=None, nargs="*")
        parser.add_argument("-m", "--max_files", type=int, help="The maximum number of files in a single poll; <1 for unlimited", required=False, default=-1)
        parser.add_argument("-b", "--base_reader", type=str, help="The command-line of the reader for reading the files", required=False, default=None)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.dir_in = ns.dir_in
        self.dir_out = ns.dir_out
        self.poll_wait = ns.poll_wait
        self.process_wait = ns.process_wait
        self.delete_input = ns.delete_input
        self.extensions = ns.extensions
        self.other_input_files = ns.other_input_files
        self.max_files = ns.max_files
        self.base_reader = ns.base_reader

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.base_reader is None:
            return [ImageData]
        else:
            return [self.base_reader.generates()]

    def _check_dir(self, path: str, name: str):
        """
        Performs checks on the specified directory.
        Raises an exception if a problem is encountered.

        :param path: the directory to check
        :type path: str
        :param name: the name of the directory
        :type name: str
        """
        if path is None:
            raise Exception("No %s directory provided!" % name)
        if not os.path.exists(path):
            raise Exception("%s directory does not exist: %s" % (name.capitalize(), path))
        if not os.path.isdir(path):
            raise Exception("%s directory does not point to a directory: %s" % (name.capitalize(), path))

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """

        super().initialize()

        if self.poll_wait is None:
            self.poll_wait = 1.0
        if self.process_wait is None:
            self.process_wait = 0.0
        if self.delete_input is None:
            self.delete_input = False
        if (self.extensions is None) or (len(self.extensions) == 0):
            raise Exception("No extensions defined for polling!")
        if self.max_files is None:
            self.max_files = -1
        if self.base_reader is None:
            raise Exception("No base reader defined!")

        # check dirs
        self._actual_dir_in = self.session.expand_placeholders(self.dir_in)
        self._check_dir(self._actual_dir_in, "input")
        self._actual_dir_out = self.session.expand_placeholders(self.dir_out)
        self._check_dir(self._actual_dir_out, "output")

        # configure base reader
        self._base_reader = parse_reader(self.base_reader)
        if not hasattr(self._base_reader, "source"):
            raise Exception("Reader does not have 'source' attribute: %s" % str(type(self._base_reader)))
        self._base_reader.session = self.session

    def list_files(self):
        """
        Generates the list of files.

        :return: list of files
        :rtype: List[str]
        """

        file_list = []
        self.logger().debug("Start listing files: %s" % self._actual_dir_in)

        try:
            for file_name in os.listdir(self._actual_dir_in):
                file_path = os.path.join(self._actual_dir_in, file_name)

                if os.path.isdir(file_path):
                    continue

                # monitored extension?
                if self.extensions is not None:
                    ext_lower = os.path.splitext(file_name)[1]
                    if ext_lower not in self.extensions:
                        self.logger().debug("%s does not match extensions: %s" % (file_name, str(self.extensions)))
                        continue

                file_list.append(file_path)

                # reached limit for poll?
                if self.max_files > 0:
                    if len(file_list) == self.max_files:
                        self.logger().debug("Reached maximum of %d files" % self.max_files)
                        break

            self.logger().debug("Finished listing files")

        except KeyboardInterrupt:
            return
        except:
            self.logger().exception("Failed listing files!")

        return file_list

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self.logger().info("Waiting for %s seconds before polling" % str(self.poll_wait))
        sleep(self.poll_wait)
        files = self.list_files()
        result = []
        if len(files) > 0:
            if self.process_wait > 0:
                self.logger().info("Waiting for %s seconds before processing" % str(self.process_wait))
                sleep(self.process_wait)
            self._base_reader.source = files
            if isinstance(self._base_reader, Initializable):
                init_initializable(self._base_reader, "reader", raise_again=True)
            while not self._base_reader.has_finished():
                for item in self._base_reader.read():
                    result.append(item)
            self._base_reader.finalize()

        # delete or move files
        for file_path in files:
            if self.delete_input:
                self.logger().debug("Deleting input: %s" % file_path)
                os.remove(file_path)
            else:
                self.logger().debug("Moving input: %s -> %s" % (file_path, self._actual_dir_out))
                os.rename(file_path, os.path.join(self._actual_dir_out, os.path.basename(file_path)))

            # other input files?
            if self.other_input_files is not None:
                for other_input_file in self.other_input_files:
                    other_files = glob.glob(os.path.join(self._actual_dir_in, other_input_file.replace(GLOB_NAME_PLACEHOLDER, os.path.splitext(file_path)[0])))
                    for other_file in other_files:
                        other_path = os.path.join(self._actual_dir_in, other_file)
                        if self.delete_input:
                            self.logger().debug("Deleting other input: %s" % other_path)
                            os.remove(other_path)
                        else:
                            self.logger().debug("Moving other input: %s -> %s" % (other_path, self._actual_dir_out))
                            os.rename(other_path, os.path.join(self._actual_dir_out, os.path.basename(other_path)))

        for item in result:
            yield item

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return False

    def finalize(self):
        """
        Finishes the reading, e.g., for closing files or databases.
        """
        super().finalize()
        if self._base_reader is not None:
            self._base_reader.finalize()
            self._base_reader = None
