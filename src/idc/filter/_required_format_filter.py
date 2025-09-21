import abc
import argparse

from PIL import Image
from wai.logging import LOGGING_WARNING

from idc.api import REQUIRED_FORMAT_ANY, INCORRECT_FORMAT_SKIP, INCORRECT_FORMAT_ACTIONS, has_correct_format, \
    ensure_correct_format, can_process_format
from seppl.io import BatchFilter


class RequiredFormatFilter(BatchFilter, abc.ABC):
    """
    Ancestor for filters that require a specific format.
    """

    def __init__(self, incorrect_format_action: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param incorrect_format_action: how to react to incorrect input format
        :type incorrect_format_action: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.incorrect_format_action = incorrect_format_action

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-I", "--incorrect_format_action", choices=INCORRECT_FORMAT_ACTIONS, help="The action to undertake if an invalid input format is encountered.", default=INCORRECT_FORMAT_SKIP, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.incorrect_format_action = ns.incorrect_format_action

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.incorrect_format_action is None:
            self.incorrect_format_action = INCORRECT_FORMAT_SKIP

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
        return has_correct_format(image, self._required_format())

    def _ensure_correct_format(self, image: Image.Image) -> Image.Image:
        """
        Ensures that the image is in the right format.

        :param image: the image to check
        :type image: Image.Image
        :return: the image with the correct format
        :rtype: Image.Image
        """
        return ensure_correct_format(image, self._required_format())

    def _can_process(self, image: Image.Image) -> bool:
        """
        Checks whether the image can be process.
        May raise an Exception if image is of incorrect format and the action is INCORRECT_FORMAT_FAIL.

        :param image: the image to check
        :type image: Image.Image
        :return: True if the image can be processed, False if it needs to be skipped
        :rtype: bool
        """
        return can_process_format(image, self._required_format(), self.incorrect_format_action, logger=self.logger())
