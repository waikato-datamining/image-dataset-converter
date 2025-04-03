import argparse
from typing import List

from idc.api import ImageData, flatten_list, make_list, array_to_image, safe_deepcopy, ensure_grayscale, \
    grayscale_required_info
from seppl import AnyData, AliasSupporter
from seppl.io import Filter
from wai.logging import LOGGING_WARNING


class GrayscaleToBinary(Filter, AliasSupporter):
    """
    Turns RGB images into grayscale ones.
    """

    def __init__(self, threshold: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param threshold: the threshold value to use (0-255)
        :type threshold: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.threshold = threshold

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "grayscale-to-binary"

    def aliases(self) -> List[str]:
        """
        Returns the aliases under which the plugin is known under/available as well.

        :return: the aliases
        :rtype: list
        """
        return ["greyscale-to-binary"]

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Turns grayscale images into binary ones. " + grayscale_required_info()

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
        parser.add_argument("-t", "--threshold", type=int, help="The threshold to use (0-255).", required=False, default=127)
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
            self.threshold = 127

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for gray_item in make_list(data):
            img = ensure_grayscale(gray_item.image, self.logger())
            # apply threshold
            binary_img = img.point(lambda p: 255 if p > self.threshold else 0, '1')
            binary_item = type(gray_item)(source=None, image_name=gray_item.image_name,
                                          data=array_to_image(binary_img, gray_item.image_format)[1].getvalue(),
                                          image=binary_img, image_format=gray_item.image_format,
                                          metadata=safe_deepcopy(gray_item.get_metadata()),
                                          annotation=safe_deepcopy(gray_item.annotation))
            result.append(binary_item)

        return flatten_list(result)
