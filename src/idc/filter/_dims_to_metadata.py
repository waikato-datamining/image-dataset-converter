import argparse
from typing import List

from seppl import AnyData
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, flatten_list
from idc.api import ImageData

DEFAULT_WIDTH_FIELD = "width"
DEFAULT_HEIGHT_FIELD = "height"


class DimensionToMetadata(BatchFilter):
    """
    Transfers the image dimensions to the meta-data.
    """

    def __init__(self, width_field: str = None, height_field: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param width_field: the meta-data field to use for storing the width
        :type width_field: str
        :param height_field: the meta-data field to use for storing the height
        :type height_field: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.width_field = width_field
        self.height_field = height_field

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "dims-to-metadata"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Transfers the image dimensions to the meta-data."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

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
        parser.add_argument("--width_field", metavar="FIELD", type=str, default=DEFAULT_WIDTH_FIELD, help="The metadata field for the width", required=False)
        parser.add_argument("--height_field", metavar="FIELD", type=str, default=DEFAULT_HEIGHT_FIELD, help="The metadata field for the height", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.width_field = ns.width_field
        self.height_field = ns.height_field

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.width_field is None) or (len(self.width_field.strip()) == 0):
            self.width_field = DEFAULT_WIDTH_FIELD
        if (self.height_field is None) or (len(self.height_field.strip()) == 0):
            self.height_field = DEFAULT_HEIGHT_FIELD

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if isinstance(item, ImageData):
                item_new = item.duplicate()
                if not item_new.has_metadata():
                    self.logger().info("Initializing meta-data")
                    item_new.set_metadata(dict())
                item_new.get_metadata()[self.width_field] = item_new.image_width
                item_new.get_metadata()[self.height_field] = item_new.image_height
                result.append(item_new)
            else:
                self.logger().warning("Cannot process data type: %s" % str(type(item)))

        return flatten_list(result)
