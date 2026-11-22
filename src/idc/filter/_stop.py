from typing import Dict

from kasperl.filter import Stop as KStop
from seppl import Plugin


class Stop(KStop):
    """
    Raises an exception when the expression evaluates to True, stopping the pipeline.
    """

    def _available_data_formatters(self) -> Dict[str, Plugin]:
        """
        Returns the available data formatter plugins.

        :return: the plugins (name -> plugin)
        :rtype: dict
        """
        from idc.registry import available_data_formatters
        return available_data_formatters()
