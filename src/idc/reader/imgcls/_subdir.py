import argparse
import os
from typing import List, Iterable

from wai.logging import LOGGING_WARNING
from idc.base import ImageClassificationData
from idc.reader import Reader
from idc.writer import SplittableStreamWriter


class SubDirReader(Reader):

    def __init__(self, input_dirs: List[str] = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param input_dirs: the top-level directories to use
        :type input_dirs: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.input_dirs = input_dirs
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
        Returns a description of the handler.

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
        parser.add_argument("-i", "--input", type=str, help="Path to the directory with the sub-directories containing the images", required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.input_dirs = ns.input

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
        # find all subdirs
        self._sub_dirs = dict()
        for input_dir in self.input_dirs:
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
        input_dirs = list(self._sub_dirs.keys())
        for input_dir in input_dirs:
            for sub_dir in self._sub_dirs[input_dir]:
                for f in os.listdir(sub_dir):
                    path = os.path.join(sub_dir, f)
                    f = f.lower()
                    if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"):
                        self.logger().info("Reading image from: %s" % path)
                        yield ImageClassificationData(source=path, annotation=os.path.basename(sub_dir))
            del self._sub_dirs[input_dir]

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._sub_dirs) == 0


class SubDirWriter(SplittableStreamWriter):

    def __init__(self, output_dir: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_dir: the output directory to create the sub-dirs in
        :type output_dir: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-subdir-ic"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Saves images to sub-directories, using the classification label for the sub-directory."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to create the sub-directories in according to the image labels. Any defined splits get added beneath there.", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if not os.path.exists(self.output_dir):
            self.logger().info("Creating output dir: %s" % self.output_dir)
            os.makedirs(self.output_dir)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        if isinstance(data, ImageClassificationData):
            data = [data]

        for item in data:
            sub_dir = self.output_dir
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if item.annotation is not None:
                sub_dir = os.path.join(sub_dir, item.annotation)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating sub dir: %s" % sub_dir)
                os.makedirs(sub_dir)
            path = os.path.join(sub_dir, item.image_name())
            self.logger().info("Writing image to: %s" % path)
            item.save_image(path)
