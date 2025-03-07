import argparse
from typing import List

import numpy as np
from PIL import Image
from seppl import AnyData, AliasSupporter
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, flatten_list, make_list, array_to_image, safe_deepcopy

CONVERSION_BT601 = "BT.601"
CONVERSION_BT709 = "BT.709"
CONVERSION_BT2020 = "BT.2020"
CONVERSIONS = [
    CONVERSION_BT601,
    CONVERSION_BT709,
    CONVERSION_BT2020,
]
CONVERSION_PARAMETERS = {
    CONVERSION_BT601: [0.2989, 0.5870, 0.1140],
    CONVERSION_BT709: [0.2126, 0.7152, 0.0722],
    CONVERSION_BT2020: [0.2627, 0.678, 0.0593],
}
CONVERSION_INFO = {
    CONVERSION_BT601: "https://en.wikipedia.org/wiki/Rec._601",
    CONVERSION_BT709: "https://en.wikipedia.org/wiki/Rec._709",
    CONVERSION_BT2020: "https://en.wikipedia.org/wiki/Rec._2020",
}


class RGBToGrayscale(Filter, AliasSupporter):
    """
    Turns RGB images into grayscale ones.
    """

    def __init__(self, conversion: str = CONVERSION_BT601,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param conversion: the conversion to use, BT601 by default
        :type conversion: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.conversion = conversion

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "rgb-to-grayscale"

    def aliases(self) -> List[str]:
        """
        Returns the aliases under which the plugin is known under/available as well.

        :return: the aliases
        :rtype: list
        """
        return ["rgb-to-greyscale"]

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Turns RGB images into grayscale ones.\n" \
            + "\n".join(["%s: %s" % (x, CONVERSION_INFO[x]) for x in CONVERSIONS])

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
        return [AnyData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-c", "--conversion", choices=CONVERSIONS, help="The conversion to apply.", required=False, default=CONVERSION_BT601)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.conversion = ns.conversion

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.conversion is None:
            self.conversion = CONVERSION_BT601
        if self.conversion not in CONVERSIONS:
            raise Exception("Unknown conversion (available: %s): %s" % ("|".join(CONVERSIONS), self.conversion))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for rgb_item in make_list(data):
            rgb_array = np.array(rgb_item.image)
            gray_array = np.dot(rgb_array[..., :3], CONVERSION_PARAMETERS[self.conversion])
            gray_img = Image.fromarray(np.uint8(gray_array), mode='L')
            gray_item = type(rgb_item)(source=None, image_name=rgb_item.image_name,
                                       data=array_to_image(gray_array, rgb_item.image_format),
                                       image=gray_img, image_format=rgb_item.image_format,
                                       metadata=safe_deepcopy(rgb_item.get_metadata()),
                                       annotation=safe_deepcopy(rgb_item.annotation))
            result.append(gray_item)

        return flatten_list(result)
