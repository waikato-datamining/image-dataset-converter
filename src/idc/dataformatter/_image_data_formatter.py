import argparse

from wai.logging import LOGGING_WARNING

from kasperl.api import DataFormatter

PH_DATA = "data"
PH_IMAGE_NAME = "image-name"
PH_IMAGE_FORMAT = "image-format"
PH_IMAGE_WIDTH = "image-width"
PH_IMAGE_HEIGHT = "image-height"
PH_HAS_ANNOTATIONS = "has-annotations"
PH_ANNOTATIONS = "annotations"
PLACEHOLDERS = [
    PH_DATA,
    PH_IMAGE_NAME,
    PH_IMAGE_FORMAT,
    PH_IMAGE_WIDTH,
    PH_IMAGE_HEIGHT,
    PH_HAS_ANNOTATIONS,
    PH_ANNOTATIONS,
]


class ImageDataFormatter(DataFormatter):

    def __init__(self, output_format: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_format: the format for the output
        :type output_format: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_format = output_format

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "df-image-data"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Expands the placeholders in the format string using the available image data."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--output_format", type=str, help="The format to use for the output, available placeholders: %s" % ", ".join(PLACEHOLDERS), required=False, default="{" + PH_DATA + "}")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_format = ns.output_format

    def format_data(self, data) -> str:
        """
        Turns the data into a formatted string.

        :param data: the data to format
        :return: the generated string
        :rtype: str
        """
        result = self.output_format

        for ph in PLACEHOLDERS:
            ph_full = "{" + ph + "}"
            if ph_full in result:
                value = None
                if ph == PH_DATA:
                    value = str(data)
                elif ph == PH_IMAGE_NAME:
                    value = data.image_name
                elif ph == PH_IMAGE_FORMAT:
                    value = data.image_format
                elif ph == PH_IMAGE_WIDTH:
                    value = str(data.image_width)
                elif ph == PH_IMAGE_HEIGHT:
                    value = str(data.image_height)
                elif ph == PH_HAS_ANNOTATIONS:
                    value = str(data.has_annotation())
                elif ph == PH_ANNOTATIONS:
                    value = str(data.get_annotation())
                if value is None:
                    self.logger().warning("Unsupported placeholder: {%s}" % ph_full)
                else:
                    result = result.replace(ph_full, value)

        return result
