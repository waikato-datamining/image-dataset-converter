import argparse
import os
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, get_object_label, make_list

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_COMMASEP = "comma-separated"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_COMMASEP,
]


class WriteLabels(Filter):
    """
    Collects labels passing through and writes them to the specified file (stdout if not provided).
    """

    def __init__(self, output_file: str = None, output_format: str = OUTPUT_FORMAT_TEXT,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param output_file: the file to write the labels to
        :type output_file: str
        :param output_format: the format to use
        :type output_format: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_format = output_format
        self._labels = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "write-labels"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Collects labels passing through and writes them to the specified file (stdout if not provided)."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData, ImageClassificationData, ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData, ImageClassificationData, ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, default=None, help="The file to write the labels to; uses stdout if not provided", required=False)
        parser.add_argument("-f", "--output_format", choices=OUTPUT_FORMATS, default=OUTPUT_FORMAT_TEXT, help="The format to use for the labels", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.output_format = ns.output_format

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._labels = set()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        for item in make_list(data):
            if not item.has_annotation():
                continue

            if isinstance(item, ImageClassificationData):
                self._labels.add(item.annotation)
            elif isinstance(item, ObjectDetectionData):
                for obj in item.annotation:
                    label = get_object_label(obj)
                    if label is not None:
                        self._labels.add(label)
            elif isinstance(item, ImageClassificationData):
                for label in item.annotation.layers:
                    self._labels.add(label)

        return data

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        labels = sorted(self._labels)
        if self.output_format == OUTPUT_FORMAT_TEXT:
            text = "\n".join(labels)
        elif self.output_format == OUTPUT_FORMAT_COMMASEP:
            text = ",".join(labels)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

        if (self.output_file is None) or os.path.isdir(self.output_file):
            print(text)
        else:
            self.logger().info("Writing labels to: %s" % self.output_file)
            with open(self.output_file, "w") as fp:
                fp.write(text)
                fp.write("\n")
