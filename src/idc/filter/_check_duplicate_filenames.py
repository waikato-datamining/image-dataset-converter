from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ImageData


class CheckDuplicateFilenames(Filter):
    """
    Ensures that file names are unique (raises an exception if not).
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
        self._names = None
        self._paths = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "check-duplicate-filenames"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Ensures that file names are unique (raises an exception if not)."

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

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._names = set()
        self._paths = dict()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record or None if to drop
        """
        result = []

        if isinstance(data, ImageData):
            data = [data]

        for item in data:
            if item.image_name in self._names:
                msg = "File name already encountered: %s" % item.image_name
                if item.source is not None:
                    msg += "\n- full path: %s" % item.source
                if item.image_name in self._paths:
                    msg += "\n- previous file: %s" % self._paths[item.image_name]
                raise Exception(msg)
            self._names.add(item.image_name)
            if item.source is not None:
                self._paths[item.image_name] = item.source

        if len(result) == 1:
            result = result[0]

        return result
