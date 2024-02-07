from typing import List

from seppl import get_class_name
from seppl.io import Filter
from idc.base import ImageData
from idc.base.imgcls import ImageClassificationData


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
        return [ImageData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageData, ImageClassificationData]

    def _do_process(self, data: ImageData):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        if isinstance(data, ImageData):
            data.annotation = None
        else:
            self.logger().warning("Expected %s but got %s instead, failed to strip annotations!"
                                  % (get_class_name(ImageData), get_class_name(data)))
        return data
