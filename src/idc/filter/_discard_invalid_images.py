from typing import List

from idc.api import ImageData
from kasperl.api import make_list, flatten_list
from seppl import AnyData
from ._discard_filter import DiscardFilter


class DiscardInvalidImages(DiscardFilter):
    """
    Discards invalid images, e.g., stemming from corrupt files.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "discard-invalid-images"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Discards invalid images, e.g., stemming from corrupt files."

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
            keep = True
            try:
                if item.image is None:
                    keep = False
            except:
                keep = False

            if keep:
                self._keep(item)
                result.append(item)
            else:
                self._discard(item)

        return flatten_list(result)
