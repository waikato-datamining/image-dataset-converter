from typing import Dict, List

from wai.logging import LOGGING_WARNING
from seppl import Plugin
from kasperl.reader import WatchDir as KWatchDir


class WatchDir(KWatchDir):

    def __init__(self, dir_in: str = None, dir_out: str = None, check_wait: float = None, process_wait: float = None,
                 action: str = None, extensions: List[str] = None,
                 other_input_files: List[str] = None, max_files: int = None, base_reader: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param dir_in: the directory to poll for new files
        :type dir_in: str
        :param dir_out: the directory to move the files to before presenting them to the base reader
        :type dir_out: str
        :param check_wait: the seconds to wait before checking whether any files have been discovered
        :type check_wait: float
        :param process_wait: the seconds to wait before processing the files (e.g., to be fully written to disk)
        :type process_wait: float
        :param action: the action to apply to the input files
        :type action: str
        :param extensions: the list of extensions to poll the directory for
        :type extensions: list
        :param other_input_files: other files that need to be present, glob expression (use placeholder GLOB_NAME_PLACEHOLDER)
        :type other_input_files: list
        :param max_files: the maximum number of files to poll (<1 for no limit)
        :type max_files: int
        :param base_reader: the base reader to use (command-line)
        :type base_reader: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(dir_in=dir_in, dir_out=dir_out, check_wait=check_wait, process_wait=process_wait,
                         action=action, extensions=extensions, other_input_files=other_input_files,
                         max_files=max_files, base_reader=base_reader,
                         logger_name=logger_name, logging_level=logging_level)

    def _available_readers(self) -> Dict[str, Plugin]:
        """
        Return the available readers.

        :return: the reader plugins
        :rtype: dict
        """
        from idc.registry import available_readers
        return available_readers()
