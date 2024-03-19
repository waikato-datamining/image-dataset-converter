from typing import List

from seppl import get_class_name, AnyData
from seppl.io import Filter

from idc.api import ImageData, flatten_list, make_list


class StripAnnotations(Filter):

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "strip-annotations"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Removes all annotations from the data coming through."

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

    def _do_process(self, data: ImageData):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if isinstance(item, ImageData):
                data = data.duplicate()
                data.annotation = None
                result.append(data)
            else:
                self.logger().warning("Expected %s but got %s instead, failed to strip annotations!"
                                      % (get_class_name(ImageData), get_class_name(data)))

        return flatten_list(result)
