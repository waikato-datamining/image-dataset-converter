import argparse
import os
from typing import List

from wai.logging import LOGGING_WARNING

from idc.api import ImageSegmentationData, SplittableStreamWriter, make_list, \
    AnnotationsOnlyWriter, add_annotations_only_param, to_indexedpng
from simple_palette_utils import generate_palette_list, PALETTE_AUTO, palettes
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class IndexedPngImageSegmentationWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None,
                 image_path_rel: str = None, palette: str = None, annotations_only: bool = None, background: int = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param image_path_rel: the relative path from the annotations to the images
        :type image_path_rel: str
        :param palette: the palette to use, either a supported palette name (auto|x11|light|dark) or comma-separated list of R,G,B values
        :type palette: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
        :param background: the index (0-255) to use as background
        :type background: int
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
        self.image_path_rel = image_path_rel
        self.palette = palette
        self.annotations_only = annotations_only
        self.background = background
        self._palette_list = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-indexed-png-is"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the annotations as indexed PNG files. The associated JPG images can be placed in folder relative to the annotation."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--image_path_rel", metavar="PATH", type=str, default=None, help="The relative path from the annotations to the images directory", required=False)
        parser.add_argument("-p", "--palette", metavar="PALETTE", type=str, default=PALETTE_AUTO, help="The palette to use; either palette name (%s) or comma-separated list of R,G,B values." % "|".join(palettes()), required=False)
        parser.add_argument("--background", type=int, help="The index (0-255) to use for the background", required=False, default=0)
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
        self.image_path_rel = ns.image_path_rel
        self.palette = ns.palette
        self.annotations_only = ns.annotations_only
        self.background = ns.background

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageSegmentationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.image_path_rel is None:
            self.image_path_rel = ""
        self._palette_list = generate_palette_list(self.palette)
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

            # image
            path = sub_dir
            if len(self.image_path_rel) > 0:
                path = os.path.join(path, self.image_path_rel)
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # annotations
            if item.has_annotation():
                ann = to_indexedpng(item.image_width, item.image_height, item.annotation, self._palette_list, background=self.background)
                path = sub_dir
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, item.image_name)
                path = os.path.splitext(path)[0] + ".png"
                self.logger().info("Writing annotations to: %s" % path)
                ann.save(path)
