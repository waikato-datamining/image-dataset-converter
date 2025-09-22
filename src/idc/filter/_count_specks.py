import argparse
import cv2
from typing import List

import numpy as np
from wai.logging import LOGGING_WARNING

from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, binary_required_info, REQUIRED_FORMAT_BINARY
from idc.filter import ImageAndAnnotationFilter


class CountSpecks(ImageAndAnnotationFilter):
    """
    Counts the number of small specks in the image.
    """

    def __init__(self, apply_to: str = None, output_format: str = None, incorrect_format_action: str = None,
                 max_area: float = None, invert: bool = False, metadata_key: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param apply_to: where to apply the filter to
        :type apply_to: str
        :param output_format: the output format to use
        :type output_format: str
        :param incorrect_format_action: how to react to incorrect input format
        :type incorrect_format_action: str
        :param max_area: the maximum area for the specks
        :type max_area: float
        :param invert: whether to invert the binary image
        :type invert: bool
        :param metadata_key: the meta-data key for storing the count in
        :type metadata_key: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(apply_to=apply_to, output_format=output_format, incorrect_format_action=incorrect_format_action,
                         logger_name=logger_name, logging_level=logging_level)
        self.max_area = max_area
        self.invert = invert
        self.metadata_key = metadata_key
        self._count = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "count-specks"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Counts the number of small specks in the image. " + binary_required_info()

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData, ObjectDetectionData, ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData, ObjectDetectionData, ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-M", "--max_area", type=float, help="The maximum area for the specks in order to count them.", default=2.0, required=False)
        parser.add_argument("-i", "--invert", action="store_true", help="Whether to invert the binary image, i.e., looking for black specks rather than white ones.")
        parser.add_argument("-k", "--metadata_key", type=str, help="The key in the meta-data to store the count under.", default="speck-count", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.max_area = ns.max_area
        self.invert = ns.invert
        self.metadata_key = ns.metadata_key

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.max_area is None:
            self.max_area = 2.0
        if self.max_area < 1:
            raise Exception("Area must be least 1, current: %s" % str(self.max_area))
        if self.invert is None:
            self.invert = False
        if self.metadata_key is None:
            self.metadata_key = "speck-count"

    def _required_format(self) -> str:
        """
        Returns what input format is required for applying the filter.

        :return: the type of image
        :rtype: str
        """
        return REQUIRED_FORMAT_BINARY

    def _pre_apply_filter(self, item):
        """
        Hook method that gets executed before the filter is being applied the first time.

        :param item: the current image data being processed
        """
        self._count = 0

    def _apply_filter(self, source: str, array: np.ndarray) -> np.ndarray:
        """
        Applies the filter to the image and returns the numpy array.

        :param source: whether image or layer
        :type source: str
        :param array: the image the filter to apply to
        :type array: np.ndarray
        :return: the filtered image
        :rtype: np.ndarray
        """
        current = array
        if self.invert:
            current ^= 255  # take from here: https://stackoverflow.com/a/15901351/4698227
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(current, connectivity=8)
        for i in range(1, num_labels):  # skip background (i=0)
            area = stats[i, cv2.CC_STAT_AREA]
            if area <= self.max_area:
                self._count += 1

        return array

    def _post_apply_filter(self, item):
        """
        Hook method that gets executed after the filter has been applied the last time.

        :param item: the updated image data
        """
        if not item.has_metadata():
            item.set_metadata(dict())
        item.get_metadata()[self.metadata_key] = self._count
        self.logger().info("# specks with area <= %f: %d" % (self.max_area, self._count))
