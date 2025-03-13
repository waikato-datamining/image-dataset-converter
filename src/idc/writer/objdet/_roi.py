import argparse
import csv
import os
from typing import List

from wai.common.adams.imaging.locateobjects import absolute_to_normalized
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, SplittableStreamWriter, make_list, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class ROIObjectDetectionWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, suffix: str = "-rois.csv", size_mode: bool = False,
                 annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/csv in
        :type output_dir: str
        :param suffix: the suffix of the ROI CSV files (eg -rois.csv)
        :type suffix: str
        :param size_mode: whether to output w/h rather than x1/y1
        :type size_mode: bool
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
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
        self.suffix = suffix
        self.size_mode = size_mode
        self.annotations_only = annotations_only
        self._label_mapping = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-roicsv-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box/polygon definitions in a ROI .csv file alongside the image."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.csv files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("-s", "--suffix", metavar="SUFFIX", type=str, default="-rois.csv", help="The suffix used by the ROI CSV files.", required=False)
        parser.add_argument("--size_mode", action="store_true", help="Whether to output w/h rather than x1/y1.", required=False)
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
        self.suffix = ns.suffix
        self.size_mode = ns.size_mode
        self.annotations_only = ns.annotations_only

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
        if self.annotations_only is None:
            self.annotations_only = False
        self._label_mapping = dict()

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

            path = os.path.join(sub_dir, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            if item.has_annotation():
                path = os.path.splitext(path)[0] + self.suffix
                self.logger().info("Writing ROI CSV to: %s" % path)
                aobjs = item.annotation
                width, height = item.image_size
                nobjs = absolute_to_normalized(aobjs, width, height)
                if self.size_mode:
                    fields = ["file", "x", "y", "w", "h", "xn", "yn", "wn", "hn", "label", "label_str", "score", "poly_x", "poly_y", "poly_xn", "poly_yn", "minrect_w", "minrect_h"]
                else:
                    fields = ["file", "x0", "y0", "x1", "y1", "x0n", "y0n", "x1n", "y1n", "label", "label_str", "score", "poly_x", "poly_y", "poly_xn", "poly_yn", "minrect_w", "minrect_h"]
                with open(path, "w") as fp:
                    writer = csv.DictWriter(fp, fields)
                    writer.writeheader()
                    for aobj, nobj in zip(aobjs, nobjs):
                        if "type" in aobj.metadata:
                            label_str = aobj.metadata["type"]
                            if label_str not in self._label_mapping:
                                self._label_mapping[label_str] = len(self._label_mapping)
                            label = self._label_mapping[label_str]
                        else:
                            label_str = ""
                            label = ""
                        row = dict()
                        row["file"] = item.image_name
                        if self.size_mode:
                            row["x"] = aobj.x
                            row["y"] = aobj.y
                            row["h"] = aobj.width
                            row["y"] = aobj.height
                            row["xn"] = nobj.x
                            row["yn"] = nobj.y
                            row["wn"] = nobj.width
                            row["hn"] = nobj.height
                        else:
                            row["x0"] = aobj.x
                            row["y0"] = aobj.y
                            row["x1"] = aobj.x + aobj.width - 1
                            row["y1"] = aobj.y + aobj.height - 1
                            row["x0n"] = nobj.x
                            row["y0n"] = nobj.y
                            row["x1n"] = nobj.x + nobj.width
                            row["y1n"] = nobj.y + nobj.height
                        row["label"] = label
                        row["label_str"] = label_str
                        if "score" in aobj.metadata:
                            row["score"] = aobj.metadata["score"]
                        if aobj.has_polygon():
                            row["poly_x"] = ",".join([str(x) for x in aobj.get_polygon_x()])
                            row["poly_y"] = ",".join([str(y) for y in aobj.get_polygon_y()])
                            row["poly_xn"] = ",".join(["%.6f" % x for x in nobj.get_polygon_x()])
                            row["poly_yn"] = ",".join(["%.6f" % y for y in nobj.get_polygon_y()])
                        if "minrect_w" in aobj.metadata:
                            row["minrect_w"] = aobj.metadata["minrect_w"]
                        if "minrect_h" in aobj.metadata:
                            row["minrect_h"] = aobj.metadata["minrect_h"]
                        writer.writerow(row)
