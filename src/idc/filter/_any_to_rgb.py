from typing import List

from idc.api import ImageData, flatten_list, make_list, array_to_image, safe_deepcopy
from seppl import AnyData
from seppl.io import Filter


class AnyToRGB(Filter):
    """
    Turns any image type into an RGB one.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "any-to-rgb"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Turns any image type into an RGB one."

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
        for any_item in make_list(data):
            rgb_image = any_item.image.convert("RGB")
            rgb_item = type(any_item)(source=None, image_name=any_item.image_name,
                                      data=array_to_image(rgb_image, any_item.image_format)[1].getvalue(),
                                      image=rgb_image, image_format=any_item.image_format,
                                      metadata=safe_deepcopy(any_item.get_metadata()),
                                      annotation=safe_deepcopy(any_item.annotation))
            result.append(rgb_item)

        return flatten_list(result)
