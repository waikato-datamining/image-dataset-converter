import argparse
import os
from typing import List

from wai.logging import LOGGING_WARNING
from wai.common.file.report import Report, Field, save
from idc.api import ObjectDetectionData, SplittableStreamWriter, make_list


class AdamsObjectDetectionWriter(SplittableStreamWriter):

    def __init__(self, output_dir: str = None, prefix: str = "Object.",
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param prefix: the field name prefix to use for storing bbox/polygon definitions in the report files
        :type prefix: str
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
        self.prefix = prefix

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-adams-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box/polygon definitions in an ADAMS .report file alongside the image."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.report files in. Any defined splits get added beneath there.", required=True)
        parser.add_argument("-p", "--prefix", metavar="PREFIX", type=str, default="Object.", help="The field prefix to use in the .report files for identifying bbox/polygon object definitions", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.prefix = ns.prefix

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

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
        for item in make_list(data):
            sub_dir = self.output_dir
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating sub dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            report = Report()
            empty = True
            if item.has_annotation():
                empty = False
                report = item.get_absolute().to_report(prefix=self.prefix)
            if item.has_metadata():
                for k in item.get_metadata():
                    empty = False
                    report.set_value(Field.parse_field(k), item.get_metadata()[k])

            path = os.path.join(sub_dir, item.image_name)
            self.logger().info("Writing image to: %s" % path)
            item.save_image(path)

            if not empty:
                path = os.path.splitext(path)[0] + ".report"
                self.logger().info("Writing report to: %s" % path)
                save(report, path)
