from typing import Any

from kasperl.filter import SanitizeName as KSanitizeName


class SanitizeName(KSanitizeName):

    def _duplicate(self, item: Any, path: str, name_new: str) -> Any:
        """
        Duplicates the data item using the new name.

        :param item: the item to duplicate
        :param path: the path of the item
        :type path: str
        :param name_new: the new name
        :type name_new: str
        :return: the duplicated item
        """
        return item.duplicate(source=None, force_no_source=True, name=name_new)
