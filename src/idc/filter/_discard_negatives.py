from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, flatten_list, AnnotationHandler


class DiscardNegatives(Filter):
    """
    Discards negative records, i.e., ones without annotations.
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
        self.kept = 0
        self.discarded = 0

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "discard-negatives"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Discards negative records, i.e., ones without annotations."

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

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self.kept = 0
        self.discarded = 0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if not isinstance(item, AnnotationHandler):
                self.logger().warning("Not implementing '%s', cannot access annotations, keeping therefore!" % str(AnnotationHandler))
                result.append(item)
                continue

            if item.has_annotation():
                self.kept += 1
                result.append(item)
            else:
                self.discarded += 1
                self.logger().info("Discarding: %s" % str(item))

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.logger().info("# kept: %d" % self.kept)
        self.logger().info("# discarded: %d" % self.discarded)
