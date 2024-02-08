import argparse
import os
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report, Field, loadf, save
from seppl.io import locate_files
from idc.base import ObjectDetectionData, locate_image
from idc.reader import Reader
from idc.writer import SplittableStreamWriter


class AdamsObjectDetectionReader(Reader):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 prefix: str = "Object.", logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param prefix: the field name prefix to use for locating bbox/polygon definitions in the report files
        :type prefix: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.prefix = prefix
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-adams-od"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box and/or polygon definitions from the associated .report file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the report file(s) to read; glob syntax is supported", required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the report files to use", required=False, nargs="*")
        parser.add_argument("-p", "--prefix", metavar="PREFIX", type=str, default="Object.", help="The field prefix in the .report files that identifies bbox/polygon object definitions", required=False)
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
        self.prefix = ns.prefix

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.prefix is None:
            raise Exception("No prefix defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self.finalize()

        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        report = loadf(self._current_input)
        annotations = LocatedObjects.from_report(report, self.prefix)

        meta = dict()
        for field in report:
            if field.name.startswith(self.prefix):
                continue
            meta[field.to_parseable_string()] = report.get_value(field)
        if len(meta) == 0:
            meta = None

        image = locate_image(self._current_input)
        if image is None:
            self.logger().warning("No associated image found: %s" % self._current_input)
            yield None
        yield ObjectDetectionData(source=image, annotation=annotations, metadata=meta)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0

    def finalize(self):
        """
        Finishes the reading, e.g., for closing files or databases.
        """
        if self._current_input is not None:
            super().finalize()
            self._current_input = None


class AdamsImageClassificationWriter(SplittableStreamWriter):

    def __init__(self, output_dir: str = None, prefix: str = "Object.",
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

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
        Returns a description of the handler.

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
        if isinstance(data, ObjectDetectionData):
            data = [data]

        for item in data:
            sub_dir = self.output_dir
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating sub dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            report = Report()
            empty = True
            if len(item.annotation) > 0:
                empty = False
                report = item.annotation.to_report(prefix=self.prefix)
            if item.has_metadata():
                for k in item.get_metadata():
                    empty = False
                    report.set_value(Field.parse_field(k), item.get_metadata()[k])

            path = os.path.join(sub_dir, item.image_name())
            self.logger().info("Writing image to: %s" % path)
            item.save_image(path)

            if not empty:
                path = os.path.splitext(path)[0] + ".report"
                self.logger().info("Writing report to: %s" % path)
                save(report, path)
