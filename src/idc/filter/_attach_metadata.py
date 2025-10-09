from typing import Optional

from kasperl.filter import AttachMetaData as KAttachMetaData
from idc.api import ImageData


class AttachMetaData(KAttachMetaData):

    def _get_name(self, item) -> Optional[str]:
        """
        Returns the name of the item.

        :param item: the item to get the name for
        :return: the name or None if not available
        :rtype: str or None
        """
        if isinstance(item, ImageData):
            return item.image_name
        return None
