import argparse
from typing import List

import numpy as np
from PIL import Image
from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, flatten_list, make_list, array_to_image, safe_deepcopy


class SortPixels(Filter):
    """
    Sorts the (grayscale) pixels in ascending order per row.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

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
                sorted_array = np.sort(orig_array)
                sorted_img = Image.fromarray(np.uint8(sorted_array), mode='L')
                sorted_item = type(item)(source=None, image_name=item.image_name,
                                         data=array_to_image(sorted_array, item.image_format),
                                         image=sorted_img, image_format=item.image_format,
                                         metadata=safe_deepcopy(item.get_metadata()),
                                         annotation=safe_deepcopy(item.annotation))
                result.append(sorted_item)

        return flatten_list(result)
