import argparse
from typing import List, Iterable, Union

from seppl.io import locate_files
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING

from idc.api import Reader
from idc.api import locate_file, load_image_from_file, JPEG_EXTENSIONS, \
    DepthInformation, DepthData, depth_from_grayscale


class GrayscaleDepthInfoReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 min_value: float = None, max_value: float = None,
                 image_path_rel: str = None, resume_from: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param min_value: the minimum value to use, ignored if None
        :type min_value: float
        :param max_value: the maximum value to use, ignored if None
        :type max_value: float
        :param image_path_rel: the relative path from the annotations to the images
        :type image_path_rel: str
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.min_value = min_value
        self.max_value = max_value
        self.image_path_rel = image_path_rel
        self.resume_from = resume_from
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-grayscale-dp"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the depth information from associated grayscale PNG files."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the PNG file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the PNG files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.png'", required=False)
        parser.add_argument("-m", "--min_value", type=float, help="The minimum value to use, grayscale values get offset by this.", default=None, required=False)
        parser.add_argument("-M", "--max_value", type=float, help="The maximum value to use, grayscale values 0-255 get scaled to min/max, requires min to be specified.", default=None, required=False)
        parser.add_argument("--image_path_rel", metavar="PATH", type=str, default=None, help="The relative path from the annotations to the images directory", required=False)
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
        self.min_value = ns.min_value
        self.max_value = ns.max_value
        self.image_path_rel = ns.image_path_rel
        self.resume_from = ns.resume_from

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [DepthData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.max_value is not None) and (self.min_value is None):
            raise Exception("The min value must be defined when specifying the max value!")
        if (self.min_value is not None) and (self.max_value is not None):
            if self.min_value >= self.max_value:
                raise Exception("The min value must be smaller than the max value, but got: min=%f, max=%f" % (self.min_value, self.max_value))
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.png", resume_from=self.resume_from)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input

        # associated images?
        imgs = locate_file(self.session.current_input, JPEG_EXTENSIONS, rel_path=self.image_path_rel)
        if len(imgs) == 0:
            self.logger().warning("Failed to locate associated image for: %s" % self.session.current_input)
            yield None

        # read annotations
        self.logger().info("Reading from: " + str(self.session.current_input))
        ann = load_image_from_file(self.session.current_input)
        annotations = depth_from_grayscale(ann, min_value=self.min_value, max_value=self.max_value, logger=self.logger())

        # associated image
        if len(imgs) > 1:
            self.logger().warning("Found more than one image associated with annotation, using first: %s" % imgs[0])
            yield None

        yield DepthData(source=imgs[0], annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
