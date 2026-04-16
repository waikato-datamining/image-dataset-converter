import os
from typing import Any

from kasperl.filter import Rename as KRename


class Rename(KRename):

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
        return item.duplicate(source=os.path.join(path, name_new), name=name_new)
