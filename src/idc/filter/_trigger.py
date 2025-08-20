from typing import List, Dict

from seppl import Plugin
from wai.logging import LOGGING_WARNING

from kasperl.api import COMPARISON_EQUAL
from kasperl.filter import Trigger as KTrigger


class Trigger(KTrigger):
    """
    Triggers the sub-flow with data passing through.
    """

    def __init__(self, sub_flow: List[Plugin] = None,
                 field: str = None, comparison: str = COMPARISON_EQUAL, value=None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param sub_flow: the reader/filter(s)/writer to execute
        :type sub_flow: list
        :param field: the name of the meta-data field to perform the comparison on
        :type field: str
        :param comparison: the comparison to perform
        :type comparison: str
        :param value: the value to compare with
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(sub_flow=sub_flow, field=field, comparison=comparison, value=value,
                         logger_name=logger_name, logging_level=logging_level)

    def _available_readers(self) -> Dict[str, Plugin]:
        """
        Returns the available readers from the registry.

        :return: the filters
        :rtype: dict
        """
        from idc.registry import available_readers
        return available_readers()

    def _available_filters(self) -> Dict[str, Plugin]:
        """
        Returns the available filters from the registry.

        :return: the filters
        :rtype: dict
        """
        from idc.registry import available_filters
        return available_filters()

    def _available_writers(self) -> Dict[str, Plugin]:
        """
        Returns the available writers from the registry.

        :return: the writers
        :rtype: dict
        """
        from idc.registry import available_writers
        return available_writers()
