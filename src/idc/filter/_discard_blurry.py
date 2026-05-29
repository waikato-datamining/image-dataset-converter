import argparse
import statistics
from typing import List

import cv2
import numpy as np
from wai.logging import LOGGING_WARNING

from idc.api import ImageData
from kasperl.api import make_list, flatten_list
from ._discard_filter import DiscardFilter


class DiscardBlurry(DiscardFilter):
    """
    Discards blurry images, i.e., ones with a laplacian variance that falls below the specified threshold.
    """

    def __init__(self, threshold: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param threshold: the threshold to use for the laplacian variance
        :type threshold: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.threshold = threshold
        self._variances = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "discard-blurry"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Discards blurry images, i.e., ones with a laplacian variance that falls below the specified threshold."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-t", "--threshold", metavar="NUM", type=float, default=100, help="The threshold for the laplacian variance.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.threshold = ns.threshold

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.threshold is None:
            self.threshold = 100
        self._variances = []

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            image = np.asarray(item.image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            self.logger().debug("laplacian variance: %f" % var)
            self._variances.append(var)

            if var >= self.threshold:
                self._keep(item)
                result.append(item)
            else:
                self._discard(item)

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.logger().info("min variance: %f" % min(self._variances))
        self.logger().info("max variance: %f" % max(self._variances))
        self.logger().info("mean variance: %f" % statistics.mean(self._variances))
        self.logger().info("stdev variance: %f" % statistics.stdev(self._variances))
