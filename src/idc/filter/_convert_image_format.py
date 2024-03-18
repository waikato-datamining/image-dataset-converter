import argparse
import copy
import io
import os.path
from typing import List

from wai.logging import LOGGING_WARNING
from seppl import AnyData
from seppl.io import Filter

FORMAT_JPEG = "JPEG"
FORMAT_PNG = "PNG"
FORMAT_BMP = "BMP"
FORMATS = [
    FORMAT_JPEG,
    FORMAT_PNG,
    FORMAT_BMP,
]
EXTENSIONS = {
    FORMAT_JPEG: ".jpg",
    FORMAT_PNG: ".png",
    FORMAT_BMP: ".bmp",
}


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
        :return: the potentially updated record or None if to drop
        """
        result = []

        if not isinstance(data, list):
            data = [data]

        for item in data:
            if item.image_format != self.image_format:
                # convert format
                img = item.image
                output_io = io.BytesIO()
                if img.mode is 'RGBA' or 'ARGB':
                    img = img.convert('RGB')
                img.save(output_io, format=self.image_format)
                data = output_io.getvalue()
                # update container
                item = copy.deepcopy(item)
                item.data = data
                item.image_name = os.path.splitext(item.image_name)[0] + EXTENSIONS[self.image_format]

            result.append(item)

        if len(result) == 1:
            result = result[0]

        return result