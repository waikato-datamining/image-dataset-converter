import argparse
import numpy as np
import re
from typing import List

from PIL import Image, ImageDraw
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import ObjectDetectionData, ImageSegmentationData, ImageSegmentationAnnotations, flatten_list, make_list, get_object_label


class ObjectDetectionToImageSegmentation(Filter):
    """
    Converts object detection annotations into image segmentation ones.
    """

    def __init__(self, labels: List[str] = None, regexp: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param labels: the labels to use
        :type labels: list
        :param regexp: the regular expression for using only a subset
        :type regexp: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.labels = labels
        self.regexp = regexp
        self._pattern = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "od-to-is"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Converts object detection annotations into image segmentation ones."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--labels", type=str, default=None, help="The labels to use", required=False, nargs="*")
        parser.add_argument("--regexp", type=str, default=None, help="Regular expression for using only a subset of labels", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.labels = ns.labels
        self.regexp = ns.regexp

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._pattern = re.compile(self.regexp) if (self.regexp is not None) else None
        if (self.labels is None) or (len(self.labels) == 0) and (self._pattern is None):
            raise Exception("No labels/layers or regexp defined!")

    def _label_matches(self, label: str) -> bool:
        """
        Checks whether the label matches.

        :param label:   The label to test.
        :return:        True if the label matches, false if not.
        """
        if len(self.labels) == 0 and self._pattern is None:
            return False
        elif len(self.labels) == 0:
            return bool(self._pattern.match(label))
        elif self._pattern is None:
            return label in self.labels
        else:
            return bool(self._pattern.match(label)) or label in self.labels

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            # draw bboxes/polygons
            imgs = dict()
            draws = dict()
            absolute = item.get_absolute()
            for obj in absolute:
                label = get_object_label(obj)
                if not self._label_matches(label):
                    continue
                if label not in imgs:
                    img = Image.new("1", item.image_size)
                    imgs[label] = img
                    draw = ImageDraw.Draw(img)
                    draws[label] = draw
                if obj.has_polygon():
                    points = [(x, y) for x, y in zip(obj.get_polygon_x(), obj.get_polygon_y())]
                else:
                    points = [
                        (obj.x, obj.y),
                        (obj.x + obj.width + 1, obj.y),
                        (obj.x + obj.width + 1, obj.y + obj.height + 1),
                        (obj.x, obj.y + obj.height + 1)]
                draws[label].polygon(points, fill=255, outline=255, width=1)

            # generate layers
            layers = dict()
            for label in imgs:
                layers[label] = np.asarray(imgs[label]).astype(np.uint8)
                layers[label] = np.where(layers[label] == 1, 255, 0).astype(np.uint8)

            self.logger().info("Layers generated: %s" % ",".join(sorted(layers.keys())))

            # generate imgseg container
            ann = ImageSegmentationAnnotations(labels=self.labels[:], layers=layers)
            imgseg = ImageSegmentationData(source=item.source, image_name=item.image_name, data=item.data, annotation=ann, metadata=item.get_metadata())
            result.append(imgseg)

        return flatten_list(result)
