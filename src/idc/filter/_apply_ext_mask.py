import argparse
import numpy as np
import os
from typing import List

from PIL import Image
from seppl.io import Filter
from seppl.placeholders import InputBasedPlaceholderSupporter
from wai.logging import LOGGING_WARNING

from idc.api import add_apply_to_param, APPLY_TO_IMAGE, APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH, empty_image, \
    ImageClassificationData, ObjectDetectionData
from idc.api import flatten_list, make_list, ImageData, load_image_from_file, ImageSegmentationData, DepthData
from idc.api import safe_deepcopy


class ApplyExternalMask(Filter, InputBasedPlaceholderSupporter):
    """
    Applies the binary mask loaded from an external PNG file with the same name.
    """

    def __init__(self, mask_dir: str = None, lenient: bool = None, apply_to: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mask_dir: the directory with the external masks, can contain placeholders
        :type mask_dir: str
        :param lenient: whether to be lenient, i.e., masks do not have to exist
        :type lenient: bool
        :param apply_to: what the mask gets applied to (APPLY_TO_...)
        :type apply_to: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.mask_dir = mask_dir
        self.lenient = lenient
        self.apply_to = apply_to

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "apply-ext-mask"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies the binary mask loaded from an external PNG file with the same name."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [DepthData, ImageClassificationData, ImageSegmentationData, ObjectDetectionData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [DepthData, ImageClassificationData, ImageSegmentationData, ObjectDetectionData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--mask_dir", type=str, help="The directory with the binary PNG masks to load from, can contain placeholders.", default=None, required=True)
        parser.add_argument("--lenient", action="store_true", help="Missing mask files or incorrect file formats will not generate an error when set.")
        add_apply_to_param(parser, default=APPLY_TO_BOTH)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.mask_dir = ns.mask_dir
        self.lenient = ns.lenient
        self.apply_to = ns.apply_to

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.mask_dir is None) or (len(self.mask_dir) == 0):
            raise Exception("No mask directory defined!")
        if self.lenient is None:
            self.lenient = False
        if self.apply_to is None:
            self.apply_to = APPLY_TO_BOTH

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            path = self.session.expand_placeholders(self.mask_dir)
            path = os.path.join(path, os.path.splitext(os.path.basename(self.session.current_input))[0] + ".png")
            if not os.path.exists(path) or not os.path.isfile(path):
                if self.lenient:
                    self.logger().warning("Mask not found, skipping: %s" % path)
                    result.append(result)
                    continue
                else:
                    raise IOError("Failed to locate mask: %s" % path)

            self.logger().info("Loading mask: %s" % path)
            mask = load_image_from_file(path)
            if mask.mode != 'L':
                # only output warning if not binary
                if mask.mode != '1':
                    self.logger().warning("Converting mask from '%s' to grayscale: %s" % (mask.mode, path))
                mask = mask.convert('L')
                # ensure we have 0/255 values
                arr = np.asarray(mask)
                arr = np.where(arr > 0, 255, arr)
                mask = Image.fromarray(np.uint8(arr))

            # check dimensions
            img = item.image
            if (mask.size[0] != img.size[0]) or (mask.size[1] != img.size[1]):
                if self.lenient:
                    self.logger().warning("Dimensions differ (image=%s, mask=%s): %s" % (str(img.size), str(mask.size), path))
                    result.append(item)
                    continue
                else:
                    raise Exception("Dimensions differ (image=%s, mask=%s): %s" % (str(img.size), str(mask.size), path))

            # image
            img_new = img
            if self.apply_to in [APPLY_TO_IMAGE, APPLY_TO_BOTH]:
                img_new = empty_image(img.mode, item.image_width, item.image_height, item.image_format)[0]
                img_new.paste(img, box=(0, 0), mask=mask)

            # annotations
            annotation_new = item.annotation
            if self.apply_to in [APPLY_TO_ANNOTATIONS, APPLY_TO_BOTH]:
                if isinstance(item, ImageSegmentationData):
                    arr = np.asarray(mask)
                    arr = np.where(arr > 0, 1, arr)
                    annotation_new = safe_deepcopy(item.annotation)
                    for layer in annotation_new.layers:
                        annotation_new[layer] = annotation_new[layer] * arr
                elif isinstance(item, DepthData):
                    arr = np.asarray(mask)
                    arr = np.where(arr > 0, 1, arr)
                    annotation_new = safe_deepcopy(item.annotation)
                    annotation_new.data = annotation_new.data * arr
                else:
                    self.logger().warning("Unsupported data container: %s" % str(type(item)))

            item_new = type(item)(image_name=item.image_name,
                                  image=img_new, image_format=item.image_format,
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=annotation_new)
            result.append(item_new)

        return flatten_list(result)
