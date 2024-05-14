from typing import List, Dict

from wai.logging import LOGGING_WARNING

from idc.api import Generator


class NullGenerator(Generator):
    """
    Outputs nothing.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "null"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Outputs nothing."

    def _do_generate(self) -> List[Dict[str, str]]:
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        return []
