import argparse
import re
from typing import List

import cv2
import numpy as np
from shapely import Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageSegmentationData, shapely_to_locatedobject
from kasperl.api import make_list, flatten_list, safe_deepcopy
from seppl.io import BatchFilter


class ImageSegmentationToObjectDetection(BatchFilter):
    """
    Converts image segmentation annotations into object detection ones.
    """

    def __init__(self, labels: List[str] = None, regexp: str = None,
                 min_size: int = None, max_size: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param labels: the labels to use
        :type labels: list
        :param regexp: the regular expression for using only a subset
        :type regexp: str
        :param min_size: the minimum width or height contours must have
        :type min_size: int
        :param max_size: the maximum width or height contours can have
        :type max_size: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.labels = labels
        self.regexp = regexp
        self.min_size = min_size
        self.max_size = max_size
        self._pattern = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "is-to-od"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Converts image segmentation annotations into object detection ones by finding " \
            + "contours in the layers that match the specified labels/regexp. Using the min/max " \
            + "parameters, contours can be filtered out that are too small or too large."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--labels", type=str, default=None, help="The labels to use", required=False, nargs="*")
        parser.add_argument("--regexp", type=str, default=None, help="Regular expression for using only a subset of labels", required=False)
        parser.add_argument("-m", "--min_size", type=int, default=None, help="The minimum width or height that detected contours must have.", required=False)
        parser.add_argument("-M", "--max_size", type=int, default=None, help="The maximum width or height that detected contours can have.", required=False)
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
        self.min_size = ns.min_size
        self.max_size = ns.max_size

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._pattern = re.compile(self.regexp) if (self.regexp is not None) else None
        if ((self.labels is None) or (len(self.labels) == 0)) and (self._pattern is None):
            raise Exception("No labels/layers or regexp defined!")

    def _check_dimension(self, dim) -> bool:
        """
        Checks whether the dimension fits the min/max size.

        :param dim: the width/height to check
        :return: True if within specified min/max
        :rtype: bool
        """
        if self.min_size is not None:
            if dim < self.min_size:
                return False
        if self.max_size is not None:
            if dim > self.max_size:
                return False
        return True

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

    def _add_contours(self, contours, ann: LocatedObjects, label: str):
        """
        Processes the contours and adds the polygons to the annotations.

        :param contours: the contours to process
        :param ann: the annotations to append
        :type ann: LocatedObjects
        :param label: the label to use
        :type label: str
        """
        for i in range(len(contours)):
            if len(contours[i]) > 2:
                polygon = Polygon(np.squeeze(contours[i]))
                # Convert invalid polygon to valid
                if not polygon.is_valid:
                    polygon = polygon.buffer(0)
                if polygon.area == 0.0:
                    continue
                lobj = shapely_to_locatedobject(polygon, label=label)
                if self.min_size is not None:
                    if not self._check_dimension(lobj.width) or not self._check_dimension(lobj.height):
                        continue
                if self.max_size is not None:
                    if not self._check_dimension(lobj.width) or not self._check_dimension(lobj.height):
                        continue
                ann.append(lobj)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann = LocatedObjects()

            if isinstance(item, ImageSegmentationData):
                for i, label in enumerate(item.annotation.labels):
                    if label not in item.annotation.layers:
                        continue
                    if not self._label_matches(label):
                        continue
                    layer = item.annotation.layers[label]
                    layer = np.where(layer > 0, 1, 0)
                    contours, _ = cv2.findContours(np.array(layer).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    self.logger().info("%s - # of contours: %s" % (label, str(len(contours))))
                    self._add_contours(contours, ann, label)
                    self.logger().info("# of polygons added: %s" % str(len(ann)))
                    item_new = ObjectDetectionData(source=item.source, image_name=item.image_name,
                                                   image=safe_deepcopy(item.image), data=safe_deepcopy(item.data),
                                                   annotation=ann, metadata=item.get_metadata())
                    result.append(item_new)
            else:
                self.logger().warning("Not an image segmentation item, cannot process: %s" % str(item))
                result.append(item)

        return flatten_list(result)
