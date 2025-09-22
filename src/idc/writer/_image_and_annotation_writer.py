import abc
import argparse

import numpy as np
from wai.logging import LOGGING_WARNING

from idc.api import ImageSegmentationData, \
    APPLY_TO_IMAGE, APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH, add_apply_to_param
from idc.writer import RequiredFormatWriter
from kasperl.api import make_list


class ImageAndAnnotationWriter(RequiredFormatWriter, abc.ABC):
    """
    Ancestor for filters that can work on either image or annotations.
    """

    def __init__(self, apply_to: str = None, incorrect_format_action: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param apply_to: where to apply the filter to
        :type apply_to: str
        :param incorrect_format_action: how to react to incorrect input format
        :type incorrect_format_action: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(incorrect_format_action=incorrect_format_action, logger_name=logger_name, logging_level=logging_level)
        self.apply_to = apply_to

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        add_apply_to_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.apply_to = ns.apply_to

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.apply_to is None:
            self.apply_to = APPLY_TO_IMAGE

    def _nothing_to_do(self, data) -> bool:
        """
        Checks whether there is nothing to do, e.g., due to parameters.

        :param data: the data to process
        :return: whether nothing needs to be done
        :rtype: bool
        """
        return False

    def _pre_apply_writer(self, item):
        """
        Hook method that gets executed before the writer is being applied the first time.

        :param item: the current image data being processed
        """
        pass

    @abc.abstractmethod
    def _apply_writer(self, source: str, array: np.ndarray):
        """
        Applies the writer to the image and returns the numpy array.

        :param source: whether image or a layer
        :type source: str
        :param array: the image to apply the writer to
        :type array: np.ndarray
        """
        raise NotImplementedError()

    def _post_apply_writer(self, item):
        """
        Hook method that gets executed after the writer has been applied the last time.

        :param item: the updated image data
        """
        pass

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        # nothing to do?
        if self._nothing_to_do(data):
            return data

        for item in make_list(data):
            self._pre_apply_writer(item)

            # apply to image
            if self.apply_to in [APPLY_TO_IMAGE, APPLY_TO_BOTH]:
                # incorrect format?
                if not self._can_process(item.image):
                    continue
                # process
                image = self._ensure_correct_format(item.image)
                array = np.asarray(image).astype(np.uint8)
                self._apply_writer("image", array)
            # apply to annotations, nothing to do for image
            else:
                np.asarray(item.image).astype(np.uint8)

            # apply to annotations?
            if isinstance(item, ImageSegmentationData) and item.has_annotation():
                if self.apply_to in [APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH]:
                    for layer in item.annotation.layers:
                        self._apply_writer(layer, item.annotation.layers[layer])

            self._post_apply_writer(item)
