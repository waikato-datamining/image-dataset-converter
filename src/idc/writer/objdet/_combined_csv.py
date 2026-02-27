import argparse
import csv
from typing import List, Iterable

from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, BatchWriter
from idc.api import ObjectDetectionData, get_object_label
from seppl.placeholders import placeholder_list, PlaceholderSupporter


class CombinedCSVObjectDetectionWriter(BatchWriter, PlaceholderSupporter):

    def __init__(self, output_file: str = None, output_polygon: bool = None, output_meta: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to save the annotations to
        :type output_file: str
        :param output_polygon: whether to output the polygon information as well
        :type output_polygon: bool
        :param output_meta: whether to output any meta-data as well
        :type output_meta: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_polygon = output_polygon
        self.output_meta = output_meta

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-combined-csv-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves all the object detection information in a single CSV file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The CSV file to store the object detection information in. " + placeholder_list(obj=self), required=True)
        parser.add_argument("-p", "--output_polygon", action="store_true", help="Whether to output any polygon information as well", required=False)
        parser.add_argument("-m", "--output_meta", action="store_true", help="Whether to output any meta-data information as well", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.output_polygon = ns.output_polygon
        self.output_meta = ns.output_meta

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
        if self.output_file is None:
            raise Exception("No output file specified!")
        if self.output_polygon is None:
            self.output_polygon = False
        if self.output_meta is None:
            self.output_meta = False

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        path = self.session.expand_placeholders(self.output_file)
        with open(path, "w") as fp:
            writer = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

            # header
            row = ["image", "label", "x", "y", "w", "h"]
            if self.output_polygon:
                row.extend(["poly_x", "poly_y"])

            meta = None
            if self.output_meta:
                meta = []
                for item in make_list(data):
                    if item.has_metadata():
                        m = item.get_metadata()
                        for k in m.keys():
                            if k not in meta:
                                meta.append(k)
                meta.sort()
                for m in meta:
                    row.append("meta-%s" % m)

            writer.writerow(row)

            # data
            for item in make_list(data):
                if not item.has_annotation():
                    self.logger().warning("No annotations: %s" % item.image_name)
                    continue

                for lobj in item.annotation:
                    row = [item.image_name, get_object_label(lobj, ""), lobj.x, lobj.y, lobj.width, lobj.height]
                    if self.output_polygon:
                        if lobj.has_polygon():
                            row.append(",".join([str(x) for x in lobj.get_polygon_x()]))
                            row.append(",".join([str(y) for y in lobj.get_polygon_y()]))
                    if self.output_meta:
                        for m in meta:
                            if m in lobj.metadata:
                                row.append(lobj.metadata[m])
                            else:
                                row.append("")
                    writer.writerow(row)
