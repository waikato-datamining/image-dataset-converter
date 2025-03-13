import argparse
import os
from collections import OrderedDict
from typing import List

from wai.logging import LOGGING_WARNING
from idc.api import ObjectDetectionData, SplittableStreamWriter, save_labels, save_labels_csv, make_list, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class YoloObjectDetectionWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None,
                 image_subdir: str = None, labels_subdir: str = None, categories: List[str] = None,
                 use_polygon_format: bool = False, labels: str = None, labels_csv: str = None,
                 annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param image_subdir: the sub-dir to use for the images
        :type image_subdir: str
        :param labels_subdir: the sub-dir to use for the labels
        :type labels_subdir: str
        :param categories: the predefined categories to use
        :type categories: str
        :param use_polygon_format: whether to use the polygon format
        :type use_polygon_format: bool
        :param labels: the text file with the comma-separated list of labels
        :type labels: str
        :param labels_csv: the CSV file to write the label mapping to (index and label)
        :type labels_csv: str
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
        self.image_subdir = image_subdir
        self.labels_subdir = labels_subdir
        self.categories = categories
        self.use_polygon_format = use_polygon_format
        self.labels = labels
        self.labels_csv = labels_csv
        self.annotations_only = annotations_only
        self._label_mapping = None  # label -> index
        self._output_dirs = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-yolo-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box/polygon definitions in YOLO .txt format. By default, places images in the 'images' subdir and the annotations in 'labels'."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.txt files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--image_subdir", metavar="DIR", type=str, default=None, help="The name of the sub-dir to use for storing the images in.", required=False)
        parser.add_argument("--labels_subdir", metavar="DIR", type=str, default=None, help="The name of the sub-dir to use for storing the annotations in.", required=False)
        parser.add_argument("-p", "--use_polygon_format", action="store_true", help="Whether to write the annotations in polygon format rather than bbox format", required=False)
        parser.add_argument("--categories", type=str, help="The predefined order of categories.", required=False, nargs="*")
        parser.add_argument("--labels", type=str, default=None, help="The text file (no path) with the comma-separated list of labels", required=False)
        parser.add_argument("--labels_csv", type=str, default=None, help="The CSV file (no path) to write the label mapping to (index and label)", required=False)
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
        self.image_subdir = ns.image_subdir
        self.labels_subdir = ns.labels_subdir
        self.categories = ns.categories
        self.use_polygon_format = ns.use_polygon_format
        self.labels = ns.labels
        self.labels_csv = ns.labels_csv
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
        if self.labels is None:
            raise Exception("No output file for labels provided!")
        if self.image_subdir is None:
            self.image_subdir = "images"
        if self.labels_subdir is None:
            self.labels_subdir = "labels"
        if self.annotations_only is None:
            self.annotations_only = False
        self._label_mapping = OrderedDict()
        if self.categories is not None:
            for i, category in enumerate(self.categories):
                self._label_mapping[category] = i
        self._output_dirs = []

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
            if sub_dir not in self._output_dirs:
                self._output_dirs.append(sub_dir)

            normalized = None
            if item.has_annotation():
                normalized = item.get_normalized()

            # image
            path = sub_dir
            if len(self.image_subdir) > 0:
                path = os.path.join(path, self.image_subdir)
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # annotations
            if normalized is not None:
                lines = []
                for obj in normalized:
                    # determine index
                    index = 0
                    if (obj.metadata is not None) and ("type" in obj.metadata):
                        label = obj.metadata["type"]
                        if label not in self._label_mapping:
                            self._label_mapping[label] = len(self._label_mapping)
                        index = self._label_mapping[label]
                    # determine coordinates
                    if self.use_polygon_format:
                        values = []
                        for x, y in zip(obj.get_polygon_x(), obj.get_polygon_y()):
                            values.append(x)
                            values.append(y)
                    else:
                        values = [obj.x + obj.width / 2, obj.y + obj.height / 2, obj.width, obj.height]
                    values = ["%.6f" % value for value in values]
                    line = str(index) + " " + " ".join(values)
                    lines.append(line)

                path = sub_dir
                if len(self.labels_subdir) > 0:
                    path = os.path.join(path, self.labels_subdir)
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, item.image_name)
                path = os.path.splitext(path)[0] + ".txt"
                self.logger().info("Writing annotations to: %s" % path)
                with open(path, "w") as fp:
                    for line in lines:
                        fp.write(line)
                        fp.write("\n")

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        for sub_dir in self._output_dirs:
            # labels
            save_labels(os.path.join(sub_dir, self.labels), self._label_mapping.keys(), logger=self.logger())

            # labels csv
            if self.labels_csv is not None:
                save_labels_csv(os.path.join(sub_dir, self.labels_csv), self._label_mapping, logger=self.logger())
