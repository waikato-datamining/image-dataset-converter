import argparse
from typing import List

import numpy as np
from PIL import Image
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import empty_image
from idc.api import flatten_list, make_list, ImageSegmentationData
from idc.api import safe_deepcopy


class ApplyLabelMask(Filter):
    """
    Applies the binary mask loaded from an external PNG file with the same name.
    """

    def __init__(self, label: str = None, lenient: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param label: the label mask to apply
        :type label: str
        :param lenient: whether to be lenient, i.e., masks do not have to exist
        :type lenient: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.label = label
        self.lenient = lenient

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "apply-label-mask"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies the specified image segmentation label mask to the base image."

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
        return [ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--label", type=str, help="The image segmentation label mask to apply to the base image.", default=None, required=True)
        parser.add_argument("--lenient", action="store_true", help="Missing labels will not generate an error.")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.label = ns.label
        self.lenient = ns.lenient

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.label is None) or (len(self.label) == 0):
            raise Exception("No label specified!")
        if self.lenient is None:
            self.lenient = False

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if not item.has_layer(self.label):
                self.logger().warning("Label '%s' not present in image '%s', skipping!" % (self.label, item.image_name))
                result.append(item)
                continue

            # create mask
            arr = item.annotation.layers[self.label]
            arr = np.where(arr > 0, 255, arr)
            mask = Image.fromarray(np.uint8(arr))

            # apply mask to image
            img = item.image
            img_new = empty_image(img.mode, item.image_width, item.image_height, item.image_format)[0]
            img_new.paste(img, box=(0, 0), mask=mask)

            item_new = type(item)(image_name=item.image_name,
                                  image=img_new, image_format=item.image_format,
                                  metadata=safe_deepcopy(item.get_metadata()),
                                  annotation=safe_deepcopy(item.annotation))
            result.append(item_new)

        return flatten_list(result)
