import argparse
from typing import List

from PIL import ExifTags
from wai.logging import LOGGING_WARNING

from idc.api import ImageData
from kasperl.api import make_list, StreamWriter
from seppl.variables import InputBasedVariableSupporter, variable_list


class ExifAutorotateInfoWriter(StreamWriter, InputBasedVariableSupporter):

    def __init__(self, output_file: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_file: the output file to save the information in
        :type output_file: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "exif-autorotate-info"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Outputs the EXIF autorotate information, if available."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The file to store the information in, uses stdout if not provided, overwrites existing files. " + variable_list(obj=self), required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            image = item.image
            image.load()
            image_exif = image.getexif()
            orientation = image_exif.get(ExifTags.Base.Orientation, 1)
            if orientation == 1:
                orientation_str = "none"
            elif orientation == 2:
                orientation_str = "flip-left-right"
            elif orientation == 3:
                orientation_str = "rotate-180"
            elif orientation == 4:
                orientation_str = "flip-top-bottom"
            elif orientation == 5:
                orientation_str = "transpose"
            elif orientation == 6:
                orientation_str = "rotate-270"
            elif orientation == 7:
                orientation_str = "transverse"
            elif orientation == 8:
                orientation_str = "rotate-90"
            else:
                orientation_str = "unknown"

            if self.output_file is None:
                print("%s: %s" % (item.image_name, orientation_str))
            else:
                path = self.session.expand_variables(self.output_file)
                self.logger().info("Writing info to: %s" % path)
                with open(path, "w") as fp:
                    fp.write(orientation_str + "\n")
