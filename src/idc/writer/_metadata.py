import argparse
import csv
import json
import os
from typing import List, Dict

from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, SplittableStreamWriter
from idc.api import ImageData
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]
OUTPUT_FORMAT_EXTENSIONS = {
    OUTPUT_FORMAT_TEXT: ".txt",
    OUTPUT_FORMAT_CSV: ".csv",
    OUTPUT_FORMAT_JSON: ".json",
}


class MetaDataWriter(SplittableStreamWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, output_format: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param output_format: the format for the output files
        :type output_format: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param split_group: the regular expression with a single group used for keeping items in the same split, e.g., for identifying the base name of a file or the sample ID
        :type split_group: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, split_group=split_group, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir
        self.output_format = output_format

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-metadata"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves just the meta-data."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the meta-data in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("-f", "--output_format", type=str, help="The format to use for the output, available formats: %s" % ", ".join(OUTPUT_FORMATS), required=False, default=OUTPUT_FORMAT_TEXT)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.output_format = ns.output_format

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def output_text(self, meta: Dict, path: str):
        """
        Outputs the meta-data in simple textual format.

        :param meta: the meta-data
        :type meta: Dict
        :param path: the file to write to
        :type path: str
        """
        keys = sorted(meta.keys())
        with open(path, "w") as f:
            f.write("Key: Value\n")
            for k in keys:
                f.write("%s: %s\n" % (k, str(meta[k])))

    def output_csv(self, meta: Dict, path: str):
        """
        Outputs the meta-data in CSV format.

        :param meta: the meta-data
        :type meta: Dict
        :param path: the file to write to
        :type path: str
        """
        keys = sorted(meta.keys())
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Key", "Value"])
            for k in keys:
                writer.writerow([k, meta[k]])

    def output_json(self, meta: Dict, path: str):
        """
        Outputs the meta-data in json format.

        :param meta: the meta-data
        :type meta: Dict
        :param path: the file to write to
        :type path: str
        """
        with open(path, "w") as f:
            json.dump(meta, f, indent=2)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next(item=item.image_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            path = os.path.join(sub_dir, item.image_name)
            path = os.path.splitext(path)[0] + OUTPUT_FORMAT_EXTENSIONS[self.output_format]
            self.logger().info("Writing meta-data to: %s" % path)
            if self.output_format == OUTPUT_FORMAT_TEXT:
                self.output_text(item.get_metadata(), path)
            elif self.output_format == OUTPUT_FORMAT_CSV:
                self.output_csv(item.get_metadata(), path)
            elif self.output_format == OUTPUT_FORMAT_JSON:
                self.output_json(item.get_metadata(), path)
            else:
                raise Exception("Unhandled output format: %s" % self.output_format)
