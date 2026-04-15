from typing import Dict

from kasperl.writer import TextFileWriter as KTextFileWriter
from seppl import Plugin
from idc.registry import available_data_formatters


class TextFileWriter(KTextFileWriter):

    def _available_data_formatters(self) -> Dict[str, Plugin]:
        """
        Returns the available data formatter plugins.

        :return: the plugins (name -> plugin)
        :rtype: dict
        """
        return available_data_formatters()
