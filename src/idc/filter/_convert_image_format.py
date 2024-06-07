import argparse
import io
import os.path
from typing import List

from wai.logging import LOGGING_WARNING
from seppl import AnyData
from seppl.io import Filter
from idc.api import flatten_list, make_list, FORMAT_EXTENSIONS, FORMATS


class ConvertImageFormat(Filter):
    """
    Converts the image format to the specified type.
    """

    def __init__(self, image_format: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param image_format: the image format to use
        :type image_format: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.image_format = image_format

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "convert-image-format"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Converts the image format to the specified type."

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
        parser.add_argument("-f", "--image_format", choices=FORMATS, help="The image format to use", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.image_format = ns.image_format

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.image_format is None:
            raise Exception("No image format provided!")
        if self.image_format not in FORMATS:
            raise Exception("Unsupported image format: %s" % self.image_format)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if item.image_format != self.image_format:
                self.logger().info("Converting %s to %s: %s" % (item.image_format, self.image_format, item.image_name))
                # convert format
                img = item.image
                output_io = io.BytesIO()
                if img.mode in ['RGBA', 'ARGB']:
                    img = img.convert('RGB')
                img.save(output_io, format=self.image_format)
                # new container
                item = type(item)(image_name=os.path.splitext(item.image_name)[0] + FORMAT_EXTENSIONS[self.image_format],
                                  data=output_io.getvalue(),
                                  metadata=item.get_metadata(), annotation=item.annotation)

            result.append(item)

        return flatten_list(result)
