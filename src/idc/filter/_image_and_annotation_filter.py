import abc
import argparse

import numpy as np
from PIL import Image
from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, flatten_list, safe_deepcopy
from idc.api import ensure_binary, ensure_grayscale, ImageSegmentationData, \
    APPLY_TO_IMAGE, APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH, add_apply_to_param, image_to_bytesio, binarize_image
from seppl.io import Filter

REQUIRED_FORMAT_ANY = "any"
REQUIRED_FORMAT_BINARY = "binary"
REQUIRED_FORMAT_GRAYSCALE = "grayscale"

INCORRECT_FORMAT_SKIP = "skip"
INCORRECT_FORMAT_FAIL = "fail"
INCORRECT_FORMAT_ACTIONS = [
    INCORRECT_FORMAT_SKIP,
    INCORRECT_FORMAT_FAIL,
]

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


class ImageAndAnnotationFilter(Filter, abc.ABC):
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
        super().__init__(logger_name=logger_name, logging_level=logging_level)
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
        parser.add_argument("-o", "--output_format", choices=OUTPUT_FORMATS, help="The image format to generate as output.", default=OUTPUT_FORMAT_ASIS, required=False)
        parser.add_argument("-I", "--incorrect_format_action", choices=INCORRECT_FORMAT_ACTIONS, help="The action to undertake if an invalid input format is encountered.", default=INCORRECT_FORMAT_SKIP, required=False)
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
        self.incorrect_format_action = ns.incorrect_format_action

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.apply_to is None:
            self.apply_to = APPLY_TO_IMAGE
        if self.output_format is None:
            self.output_format = OUTPUT_FORMAT_ASIS
        if self.incorrect_format_action is None:
            self.incorrect_format_action = INCORRECT_FORMAT_SKIP

    def _nothing_to_do(self, data) -> bool:
        """
        Checks whether there is nothing to do, e.g., due to parameters.

        :param data: the data to process
        :return: whether nothing needs to be done
        :rtype: bool
        """
        return False

    def _required_format(self) -> str:
        """
        Returns what input format is required for applying the filter.

        :return: the type of image
        :rtype: str
        """
        return REQUIRED_FORMAT_ANY

    def _has_correct_format(self, image: Image.Image) -> bool:
        """
        Checks whether the image is in the right format.

        :param image: the image to check
        :type image: Image.Image
        :return: whether the image is in the correct format
        :rtype: bool
        """
        req_format = self._required_format()
        if req_format == REQUIRED_FORMAT_ANY:
            return True
        elif req_format == REQUIRED_FORMAT_BINARY:
            return image.mode == '1'
        elif req_format == REQUIRED_FORMAT_GRAYSCALE:
            return image.mode == 'L'
        else:
            return False

    def _ensure_correct_format(self, image: Image.Image) -> Image.Image:
        """
        Ensures that the image is in the right format.

        :param image: the image to check
        :type image: Image.Image
        :return: the image with the correct format
        :rtype: Image.Image
        """
        req_format = self._required_format()
        if req_format == REQUIRED_FORMAT_ANY:
            return image
        elif req_format == REQUIRED_FORMAT_BINARY:
            return ensure_binary(image, self.logger())
        elif req_format == REQUIRED_FORMAT_GRAYSCALE:
            return ensure_grayscale(image, self.logger())
        else:
            raise Exception("Unsupported required format: %s" % req_format)

    @abc.abstractmethod
    def _apply_filter(self, array: np.ndarray) -> np.ndarray:
        """
        Applies the morphological filter to the image and returns the numpy array.

        :param array: the image the filter to apply to
        :type array: np.ndarray
        :return: the filtered image
        :rtype: np.ndarray
        """
        raise NotImplementedError()

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
            # apply to image
            if self.apply_to in [APPLY_TO_IMAGE, APPLY_TO_BOTH]:
                # incorrect format?
                if not self._has_correct_format(item.image):
                    msg = "Incorrect image format (required: %s, found: %s), skipping!" % (self._required_format(), item.image.mode)
                    if self.incorrect_format_action == INCORRECT_FORMAT_SKIP:
                        self.logger().warning(msg)
                        result.append(item)
                        continue
                    elif self.incorrect_format_action == INCORRECT_FORMAT_FAIL:
                        raise Exception(msg)
                    else:
                        raise Exception("Unhandled incorrect format action: %s" % self.incorrect_format_action)
                # process
                image = self._ensure_correct_format(item.image)
                array = np.asarray(image).astype(np.uint8)
                array_new = self._apply_filter(array)
            else:
                array_new = np.asarray(item.image).astype(np.uint8)

            # generate image/bytes
            if self.output_format == OUTPUT_FORMAT_ASIS:
                img_new = Image.fromarray(np.uint8(array_new))
            elif self.output_format == OUTPUT_FORMAT_BINARY:
                img_new = binarize_image(Image.fromarray(np.uint8(array_new)), threshold=1, logger=self.logger())
            elif self.output_format == OUTPUT_FORMAT_GRAYSCALE:
                img_new = Image.fromarray(np.uint8(array_new), mode='L')
            elif self.output_format == OUTPUT_FORMAT_RGB:
                img_new = Image.fromarray(np.uint8(array_new), mode='RGB')
            else:
                raise Exception("Unsupported output format: %s" % self.output_format)
            bytes_new = image_to_bytesio(img_new, item.image_format).getvalue()

            # apply to annotations
            annotation_new = safe_deepcopy(item.annotation)
            if isinstance(item, ImageSegmentationData) and item.has_annotation():
                if self.apply_to in [APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH]:
                    for layer in annotation_new.layers:
                        annotation_new.layers[layer] = self._apply_filter(annotation_new.layers[layer])

            item_new = type(item)(image_name=item.image_name,
                                  data=bytes_new,
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=annotation_new)
            result.append(item_new)

        return flatten_list(result)
