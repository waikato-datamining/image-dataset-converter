import argparse
import os
from typing import List

from wai.logging import LOGGING_WARNING
from wai.common.file.report import Report, Field, save
from idc.api import ImageClassificationData, SplittableStreamWriter, make_list, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class AdamsImageClassificationWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, class_field: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param class_field: the name of the field to store the classification label in
        :type class_field: str
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
        self.class_field = class_field
        self.annotations_only = annotations_only

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-adams-ic"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the classification label in an ADAMS .report file alongside the image."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.report files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("-c", "--class_field", metavar="FIELD", type=str, default=None, help="The report field containing the image classification label", required=True)
        add_annotations_only_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.class_field = ns.class_field
        self.annotations_only = ns.annotations_only

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
        if self.annotations_only is None:
            self.annotations_only = False

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            report = Report()
            empty = True
            if item.has_annotation():
                report.set_string_value(self.class_field, item.annotation)
                empty = False
            if item.has_metadata():
                for k in item.get_metadata():
                    empty = False
                    report.set_value(Field.parse_field(k), item.get_metadata()[k])

            path = os.path.join(sub_dir, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            if not empty:
                path = os.path.splitext(path)[0] + ".report"
                self.logger().info("Writing report to: %s" % path)
                save(report, path)
