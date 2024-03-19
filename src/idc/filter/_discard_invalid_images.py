from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData, flatten_list, make_list


class DiscardInvalidImages(Filter):
    """
    Discards invalid images, e.g., stemming from corrupt files.
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
        :return: the potentially updated record or None if to drop
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
                result.append(item)
            else:
                self.logger().info("Discarding image: %s" % item.image_name)

        return flatten_list(result)
