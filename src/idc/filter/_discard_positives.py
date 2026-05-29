from typing import List

from kasperl.api import make_list, flatten_list, AnnotationHandler
from seppl import AnyData
from ._discard_filter import DiscardFilter


class DiscardPositives(DiscardFilter):
    """
    Discards positive records, i.e., ones with annotations.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "discard-positives"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Discards positives records, i.e., ones with annotations."

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

            if not item.has_annotation():
                self._keep(item)
                result.append(item)
            else:
                self._discard(item)

        return flatten_list(result)
