import argparse
import os
from typing import List

from PIL import Image, ImageDraw
from wai.logging import LOGGING_WARNING
from kasperl.api import make_list, SplittableStreamWriter, AnnotationsOnlyWriter, add_annotations_only_writer_param
from idc.api import ObjectDetectionData, get_object_label
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from simple_palette_utils import generate_palette_list, PALETTE_AUTO, palettes


class InstancePngObjectDetectionWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, image_path_rel: str = None,
                 image_prefix: str = None, annotation_prefix: str = None,
                 label: str = None, palette: str = None, background: int = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param image_path_rel: the relative path from the annotations to the images
        :type image_path_rel: str
        :param image_prefix: the name prefix for the images, eg, image_
        :type image_prefix: str
        :param annotation_prefix: the name prefix for the annotations, e.g., gt_
        :type annotation_prefix: str
        :param label: the label
        :type label: str
        :param background: the index (0-255) that is used as background
        :type background: int
        :param palette: the palette to use, either a supported palette name (auto|x11|light|dark) or comma-separated list of R,G,B values
        :type palette: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
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
        self.image_path_rel = image_path_rel
        self.label = label
        self.image_prefix = image_prefix
        self.annotation_prefix = annotation_prefix
        self.palette = palette
        self.background = background
        self.annotations_only = annotations_only
        self._palette_list = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-instance-png-od"

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
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.report files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--image_path_rel", metavar="PATH", type=str, default=None, help="The relative path from the annotations to the output directory", required=False)
        parser.add_argument("--image_prefix", metavar="PREFIX", type=str, default=None, help="The prefix that the images use, e.g., 'image_'.", required=False)
        parser.add_argument("--annotation_prefix", metavar="PREFIX", type=str, default=None, help="The prefix that the annotations use, e.g., 'gt_'.", required=False)
        parser.add_argument("--label", metavar="LABEL", type=str, default=None, help="The label that the indices represent.", required=True)
        parser.add_argument("-p", "--palette", metavar="PALETTE", type=str, default=PALETTE_AUTO, help="The palette to use; either palette name (%s) or comma-separated list of R,G,B values." % "|".join(palettes()), required=False)
        parser.add_argument("--background", type=int, help="The index (0-255) that is used for the background", required=False, default=0)
        add_annotations_only_writer_param(parser)
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
        self.label = ns.label
        self.image_prefix = ns.image_prefix
        self.annotation_prefix = ns.annotation_prefix
        self.palette = ns.palette
        self.background = ns.background
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
        if self.label is None:
            raise Exception("No label defined!")
        self._palette_list = generate_palette_list(self.palette)
        if self.background is None:
            self.background = 0
        if (self.image_prefix is None) or (self.annotation_prefix is None):
            self.image_prefix = None
            self.annotation_prefix = None
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
                split = self.splitter.next(item=item.image_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            # save image
            if not self.annotations_only:
                name = item.image_name
                if (self.image_prefix is not None) and (not name.startswith(self.image_prefix)):
                    name = self.image_prefix + name
                path = os.path.join(sub_dir, name)
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # create annotations
            img = Image.new("P", item.image_size)
            img.putpalette(self._palette_list)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (item.image_width - 1, item.image_height - 1)], fill=self.background)
            color = 0
            for lobj in item.annotation:
                # correct label?
                label = get_object_label(lobj, default_label="")
                if label != self.label:
                    continue

                points = []
                if lobj.has_polygon():
                    poly_x = lobj.get_polygon_x()
                    poly_y = lobj.get_polygon_y()
                    for x, y in zip(poly_x, poly_y):
                        points.append((int(x), int(y)))
                else:
                    rect = lobj.get_rectangle()
                    points.append((int(rect.left()), int(rect.top())))
                    points.append((int(rect.right()), int(rect.top())))
                    points.append((int(rect.right()), int(rect.bottom())))
                    points.append((int(rect.left()), int(rect.bottom())))

                # skip background
                if color == self.background:
                    color += 1

                draw.polygon(tuple(points), fill=color)

                # next color
                color += 1

            # save annotations
            name = item.image_name
            if self.annotation_prefix is not None:
                if (self.image_prefix is not None) and name.startswith(self.image_prefix):
                    name = name[len(self.image_prefix):]
                name = self.annotation_prefix + name
            path = os.path.join(sub_dir, name)
            path = os.path.splitext(path)[0] + ".png"
            self.logger().info("Writing annotations to: %s" % path)
            img.save(path)
