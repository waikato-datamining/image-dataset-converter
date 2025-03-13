import argparse
import os
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from idc.api import ImageClassificationData
from idc.api import Reader


class SubDirReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the top-level directories to use
        :param source_list: the file(s) with top-level dir(s)
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self._sub_dirs = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-subdir-ic"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads images from sub-directories, uses the name of the sub-directory as classification label."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the directory with the sub-directories containing the images; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the directories to use; " + placeholder_list(obj=self), required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        # assemble top-level dirs
        all_dirs = []
        if self.source is not None:
            if isinstance(self.source, list):
                all_dirs.extend(self.source)
            else:
                all_dirs.append(self.source)
        if self.source_list is not None:
            if isinstance(self.source_list, list):
                files = self.source_list
            else:
                files = [self.source_list]
            for file in files:
                with open(file, "r") as fp:
                    lines = fp.readline()
                    lines = [x.strip() for x in lines]
                    for line in lines:
                        if len(line) == 0:
                            continue
                        if line.startswith("#"):
                            continue
                        all_dirs.append(line)

        # find all subdirs
        self._sub_dirs = dict()
        for input_dir in all_dirs:
            input_dir = self.session.expand_placeholders(input_dir)
            if not os.path.exists(input_dir):
                self.logger().warning("Directory does not exist: %s" % input_dir)
                continue
            for f in os.listdir(input_dir):
                path = os.path.join(input_dir, f)
                if os.path.isdir(path):
                    if input_dir not in self._sub_dirs:
                        self._sub_dirs[input_dir] = []
                    self._sub_dirs[input_dir].append(path)
            if input_dir not in self._sub_dirs:
                self.logger().warning("No sub-directories found in: %s" % input_dir)
            else:
                self.logger().info("Found %d sub-directories in: %s" % (len(self._sub_dirs[input_dir]), input_dir))

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        input_dirs = sorted(list(self._sub_dirs.keys()))
        for input_dir in input_dirs:
            for sub_dir in self._sub_dirs[input_dir]:
                files = []
                for f in os.listdir(sub_dir):
                    path = os.path.join(sub_dir, f)
                    f = f.lower()
                    if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"):
                        self.logger().info("Reading image from: %s" % path)
                        files.append(path)
                files = sorted(files)
                for file in files:
                    yield ImageClassificationData(source=file, annotation=os.path.basename(sub_dir))
            del self._sub_dirs[input_dir]

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._sub_dirs) == 0
