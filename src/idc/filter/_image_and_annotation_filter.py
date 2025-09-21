import abc
import argparse
import logging

import numpy as np
from PIL import Image
from wai.logging import LOGGING_WARNING

from idc.api import ImageSegmentationData, \
    APPLY_TO_IMAGE, APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH, add_apply_to_param, image_to_bytesio, binarize_image
from idc.filter import RequiredFormatFilter
from kasperl.api import make_list, flatten_list, safe_deepcopy

OUTPUT_FORMAT_ASIS = "as-is"
OUTPUT_FORMAT_BINARY = "binary"
OUTPUT_FORMAT_GRAYSCALE = "grayscale"
OUTPUT_FORMAT_RGB = "rgb"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_ASIS,
    OUTPUT_FORMAT_BINARY,
    OUTPUT_FORMAT_GRAYSCALE,
    OUTPUT_FORMAT_RGB,
]


def array_to_output_format(array: np.ndarray, output_format: str, logger: logging.Logger = None) -> Image.Image:
    """
    Turns the numpy array into the specified output format.

    :param array: the array to convert
    :type array: np.ndarray
    :param output_format: the output format to generate
    :type output_format: str
    :param logger: the optional logger to use
    :type logger: logging.Logger
    :return: the generated PIL image object
    :rtype: Image.Image
    """
    if output_format == OUTPUT_FORMAT_ASIS:
        return Image.fromarray(np.uint8(array))
    elif output_format == OUTPUT_FORMAT_BINARY:
        return binarize_image(Image.fromarray(np.uint8(array)), threshold=1, logger=logger)
    elif output_format == OUTPUT_FORMAT_GRAYSCALE:
        return Image.fromarray(np.uint8(array), mode='L')
    elif output_format == OUTPUT_FORMAT_RGB:
        return Image.fromarray(np.uint8(array), mode='RGB')
    else:
        raise Exception("Unsupported output format: %s" % output_format)


def add_output_format(parser: argparse.ArgumentParser):
    """
    Adds the -o/--output_format option to the parser.

    :param parser: the parser to append
    :type parser: argparse.ArgumentParser
    """
    parser.add_argument("-o", "--output_format", choices=OUTPUT_FORMATS, help="The image format to generate as output.", default=OUTPUT_FORMAT_ASIS, required=False)


class ImageAndAnnotationFilter(RequiredFormatFilter, abc.ABC):
    """
    Ancestor for filters that can work on either image or annotations.
    """

    def __init__(self, apply_to: str = None, output_format: str = None, incorrect_format_action: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param apply_to: where to apply the filter to
        :type apply_to: str
        :param output_format: the output format to use
        :type output_format: str
        :param incorrect_format_action: how to react to incorrect input format
        :type incorrect_format_action: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(incorrect_format_action=incorrect_format_action, logger_name=logger_name, logging_level=logging_level)
        self.apply_to = apply_to
        self.output_format = output_format
        self.incorrect_format_action = incorrect_format_action

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        add_apply_to_param(parser)
        add_output_format(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.apply_to = ns.apply_to
        self.output_format = ns.output_format

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.apply_to is None:
            self.apply_to = APPLY_TO_IMAGE
        if self.output_format is None:
            self.output_format = OUTPUT_FORMAT_ASIS

    def _nothing_to_do(self, data) -> bool:
        """
        Checks whether there is nothing to do, e.g., due to parameters.

        :param data: the data to process
        :return: whether nothing needs to be done
        :rtype: bool
        """
        return False

    def _pre_apply_filter(self, item):
        """
        Hook method that gets executed before the filter is being applied the first time.

        :param item: the current image data being processed
        """
        pass

    @abc.abstractmethod
    def _apply_filter(self, array: np.ndarray) -> np.ndarray:
        """
        Applies the filter to the image and returns the numpy array.

        :param array: the image the filter to apply to
        :type array: np.ndarray
        :return: the filtered image
        :rtype: np.ndarray
        """
        raise NotImplementedError()

    def _post_apply_filter(self, item):
        """
        Hook method that gets executed after the filter has been applied the last time.

        :param item: the updated image data
        """
        pass

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        # nothing to do?
        if self._nothing_to_do(data):
            return data

        result = []
        for item in make_list(data):
            self._pre_apply_filter(item)

            # apply to image
            if self.apply_to in [APPLY_TO_IMAGE, APPLY_TO_BOTH]:
                # incorrect format?
                if not self._can_process(item.image):
                    result.append(item)
                    continue
                # process
                image = self._ensure_correct_format(item.image)
                array = np.asarray(image).astype(np.uint8)
                array_new = self._apply_filter(array)
            # apply to annotations, nothing to do for image
            else:
                array_new = np.asarray(item.image).astype(np.uint8)

            # generate image/bytes
            img_new = array_to_output_format(array_new, self.output_format, self.logger())
            bytes_new = image_to_bytesio(img_new, item.image_format).getvalue()

            # apply to annotations?
            annotation_new = safe_deepcopy(item.annotation)
            if isinstance(item, ImageSegmentationData) and item.has_annotation():
                if self.apply_to in [APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH]:
                    for layer in annotation_new.layers:
                        annotation_new.layers[layer] = self._apply_filter(annotation_new.layers[layer])

            item_new = type(item)(image_name=item.image_name,
                                  data=bytes_new,
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=annotation_new)

            self._post_apply_filter(item_new)

            result.append(item_new)

        return flatten_list(result)
