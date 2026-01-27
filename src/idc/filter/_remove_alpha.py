from typing import List

from idc.api import ImageData, remove_alpha
from kasperl.api import make_list, flatten_list
from seppl.io import BatchFilter


class RemoveAlpha(BatchFilter):
    """
    Removes the alpha channel in the base image.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "remove-alpha"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Removes the alpha channel in the base image."

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
        return [ImageData]

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            img_new = remove_alpha(item, self.logger())
            if img_new is not None:
                item_new = item.duplicate(image=img_new)
                result.append(item_new)
            else:
                result.append(result)

        return flatten_list(result)
