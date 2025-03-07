import argparse
from typing import List

import numpy as np
from PIL import Image
from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, flatten_list, make_list, array_to_image, safe_deepcopy


SORTING_COLS = "cols"
SORTING_ROWS = "rows"
SORTING_COLS_THEN_ROWS = "cols-then-rows"
SORTING_ROWS_THEN_COLS = "rows-then-cols"
SORTING_TYPES = [
    SORTING_COLS,
    SORTING_ROWS,
    SORTING_COLS_THEN_ROWS,
    SORTING_ROWS_THEN_COLS,
]


class SortPixels(Filter):
    """
    Sorts the (grayscale) pixels in ascending order per row.
    """

    def __init__(self, sorting: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param sorting: the type of sorting to use
        :type sorting: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.sorting = sorting

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "sort-pixels"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Sorts the (grayscale) pixels in ascending order per row."

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
        parser.add_argument("-s", "--sorting", choices=SORTING_TYPES, help="How to sort the pixels.", default=SORTING_COLS, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.sorting = ns.sorting

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.sorting is None:
            self.sorting = SORTING_COLS
        if self.sorting not in SORTING_TYPES:
            raise Exception("Unsupported sorting type (%s): %s" % ("|".join(SORTING_TYPES), self.sorting))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            orig_array = np.array(item.image)
            if len(orig_array.shape) > 2:
                self.logger().warning("Expected grayscale image, but got these dimensions: %s" % str(orig_array.shape))
                result.append(item)
            else:
                if self.sorting == SORTING_COLS:
                    sorted_array = np.sort(orig_array)
                elif self.sorting == SORTING_ROWS:
                    sorted_array = np.sort(orig_array.transpose())
                elif self.sorting == SORTING_COLS_THEN_ROWS:
                    sorted_array = np.sort(orig_array)
                    sorted_array = np.sort(sorted_array.transpose())
                    sorted_array = sorted_array.transpose()
                elif self.sorting == SORTING_ROWS_THEN_COLS:
                    sorted_array = np.sort(orig_array.transpose())
                    sorted_array = np.sort(sorted_array.transpose())
                else:
                    raise Exception("Unhandled sorting type: %s" % self.sorting)
                sorted_img = Image.fromarray(np.uint8(sorted_array), mode='L')
                sorted_item = type(item)(source=None, image_name=item.image_name,
                                         data=array_to_image(sorted_array, item.image_format),
                                         image=sorted_img, image_format=item.image_format,
                                         metadata=safe_deepcopy(item.get_metadata()),
                                         annotation=safe_deepcopy(item.annotation))
                result.append(sorted_item)

        return flatten_list(result)
