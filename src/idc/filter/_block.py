from typing import Dict

from kasperl.filter import Block as KBlock
from seppl import Plugin


class Block(KBlock):
    """
    Blocks data coming through when the expression evaluates to True.
    """

    def _available_data_formatters(self) -> Dict[str, Plugin]:
        """
        Returns the available data formatter plugins.

        :return: the plugins (name -> plugin)
        :rtype: dict
        """
        from idc.registry import available_data_formatters
        return available_data_formatters()
