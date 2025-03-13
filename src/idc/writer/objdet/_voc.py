import argparse
import os
from typing import List
from xml.etree.ElementTree import Element, ElementTree

from wai.logging import LOGGING_WARNING
from idc.api import ObjectDetectionData, SplittableStreamWriter, get_object_label, make_list, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


def append_element(to: Element, tag: str, value):
    """
    Helper method to append a simple element to a parent element.

    :param to: The element to append the new element to.
    :param tag: The tag-type of the new element.
    :param value: The text content of the new element.
    """
    element = Element(tag)
    element.text = str(value)
    to.append(element)


class VOCObjectDetectionWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
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
        self.annotations_only = annotations_only

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-voc-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box definitions in PASCAL VOC .xml format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.xml files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
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

    def _append_element(self, to: Element, tag: str, value):
        """
        Helper method to append a simple element to a parent element.

        :param to: The element to append the new element to.
        :param tag: The tag-type of the new element.
        :param value: The text content of the new element.
        """
        element = Element(tag)
        element.text = str(value)
        to.append(element)

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

            absolute = None
            if item.has_annotation():
                absolute = item.get_absolute()

            # image
            path = sub_dir
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # annotations
            if absolute is not None:
                root = Element("annotation")

                append_element(root, "folder", os.path.dirname(path))
                append_element(root, "filename", os.path.basename(path))

                size = Element("size")
                root.append(size)
                append_element(size, "width", item.image_width)
                append_element(size, "height", item.image_height)
                append_element(size, "depth", 3)

                for lobj in absolute:
                    obj = Element("object")
                    root.append(obj)

                    append_element(obj, "name", get_object_label(lobj))
                    append_element(obj, "pose", "Unspecified")
                    append_element(obj, "truncated", 0)
                    append_element(obj, "difficult", 0)

                    bndbox = Element("bndbox")
                    obj.append(bndbox)
                    append_element(bndbox, "xmin", lobj.x)
                    append_element(bndbox, "ymin", lobj.y)
                    append_element(bndbox, "xmax", lobj.x + lobj.width - 1)
                    append_element(bndbox, "ymax", lobj.y + lobj.height - 1)

                path = sub_dir
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, item.image_name)
                path = os.path.splitext(path)[0] + ".xml"
                self.logger().info("Writing annotations to: %s" % path)
                tree = ElementTree(root)
                tree.write(path, "utf-8", short_empty_elements=False)
