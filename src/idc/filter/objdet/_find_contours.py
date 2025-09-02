import argparse
from typing import List

import cv2
import numpy as np
from seppl.io import Filter
from shapely import Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ensure_binary, shapely_to_locatedobject
from kasperl.api import make_list, flatten_list


class FindContours(Filter):
    """
    Finds the contours in the binary image and stores them as polygons in the annotations.
    """

    def __init__(self, label: str = None, min_size: int = None, max_size: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param label: the label to use for the detected contours
        :type label: str
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
        self.label = label
        self.min_size = min_size
        self.max_size = max_size

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "find-contours"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Finds the contours in the binary image and stores them as polygons in the annotations."

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
        return [ObjectDetectionData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--label", type=str, default=None, help="The label to use for the detected contours.", required=False)
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
        self.label = ns.label
        self.min_size = ns.min_size
        self.max_size = ns.max_size

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            binary = ensure_binary(item.image, self.logger())
            contours, _ = cv2.findContours(np.array(binary).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            self.logger().info("# of contours: %s" % str(len(contours)))

            ann = LocatedObjects()
            for i in range(len(contours)):
                if len(contours[i]) > 2:
                    polygon = Polygon(np.squeeze(contours[i]))
                    # Convert invalid polygon to valid
                    if not polygon.is_valid:
                        polygon = polygon.buffer(0)
                    lobj = shapely_to_locatedobject(polygon, label=self.label)
                    if self.min_size is not None:
                        if (lobj.width < self.min_size) or (lobj.height < self.min_size):
                            continue
                    if self.max_size is not None:
                        if (lobj.width > self.max_size) or (lobj.height > self.max_size):
                            continue
                    ann.append(lobj)
            self.logger().info("# of polygons added: %s" % str(len(ann)))
            item = item.duplicate(annotation=ann)
            result.append(item)

        return flatten_list(result)
