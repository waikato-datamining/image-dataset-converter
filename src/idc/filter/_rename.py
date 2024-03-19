import argparse
import os
from typing import List

from seppl import AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import ImageData, flatten_list, make_list

RENAME_PH_NAME = "{name}"
RENAME_PH_EXT = "{ext}"
RENAME_PH_OCCURRENCES = "{occurrences}"
RENAME_PH_COUNT = "{count}"
RENAME_PH_PDIR = "{[p]+dir}"
RENAME_PH_PDIR_SUFFIX = "pdir}"

RENAME_PLACEHOLDERS = [
    RENAME_PH_NAME,
    RENAME_PH_EXT,
    RENAME_PH_OCCURRENCES,
    RENAME_PH_COUNT,
    RENAME_PH_PDIR,
]

RENAME_PH_HELP = {
    RENAME_PH_NAME: "the name of the file, without path or extension.",
    RENAME_PH_EXT: "the extension of the file (incl dot).",
    RENAME_PH_OCCURRENCES: "the number of times this name (excl extension) has been encountered.",
    RENAME_PH_COUNT: "the number of files encountered so far.",
    RENAME_PH_PDIR: "the parent directory of the file: 'p': immediate parent, the more the p's the higher up in the hierarchy.",
}

RENAME_PH_SAME = RENAME_PH_NAME + RENAME_PH_EXT


def _format_help() -> str:
    """
    Generates the help for the name format.

    :return: the generated help
    """
    result = "Available placeholders:\n"
    for ph in RENAME_PLACEHOLDERS:
        result += "- %s: %s\n" % (ph, RENAME_PH_HELP[ph])

    return result


class Rename(Filter):
    """
    Renames files using a user-supplied format.
    """

    def __init__(self, name_format: str = RENAME_PH_SAME, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param name_format: the format to use for the file name
        :type name_format: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.name_format = name_format
        self._count = None
        self._occurrences = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "rename"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Renames files using a user-supplied format."

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
        return [AnyData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--name-format", type=str, help="The format for the new name.\n" + _format_help(), default=RENAME_PH_SAME, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.name_format = ns.name_format

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._count = 0
        self._occurrences = dict()

    def _parent_dir(self, path: str, pattern: str) -> str:
        """
        Returns the parent directory that corresponds to the pdir pattern.

        :param path: the directory path of the file
        :param pattern: the pdir pattern (without curly brackets)
        :return: the parent dir, empty string if failed to determine or too high
        """
        pattern = pattern.replace("dir", "")
        num = pattern.count("p")
        if num == 0:
            return ""
        orig_num = num
        orig_path = path
        pdir = os.path.basename(path)
        while (num > 1) and (len(path) > 0):
            path = os.path.dirname(path)
            pdir = os.path.basename(path)
            num -= 1
        if pdir == "":
            self.logger().warning("Number of parents (%d) is too high for path (%s) to generate a name!" % (orig_num, orig_path))
        return pdir

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        # nothing to do?
        if self.name_format == RENAME_PH_SAME:
            return data

        result = []
        for item in make_list(data):
            if item.source is None:
                path = "."
            else:
                path = os.path.dirname(item.source)
            name, ext = os.path.splitext(item.image_name)

            # increment counter
            self._count += 1

            # occurrences
            if name not in self._occurrences:
                self._occurrences[name] = 1
            else:
                self._occurrences[name] += 1

            # generate new name
            name_new = self.name_format
            name_new = name_new.replace(RENAME_PH_NAME, name)
            name_new = name_new.replace(RENAME_PH_EXT, ext)
            name_new = name_new.replace(RENAME_PH_COUNT, str(self._count))
            name_new = name_new.replace(RENAME_PH_OCCURRENCES, str(self._occurrences[name]))
            while RENAME_PH_PDIR_SUFFIX in name_new:
                index = name_new.index(RENAME_PH_PDIR_SUFFIX)
                start = name_new.rfind("{", 0, index)
                if start == -1:
                    self.logger().error("Found '%s' without starting '{' in name format!" % RENAME_PH_PDIR_SUFFIX)
                    break
                pattern = name_new[start + 1:index + 4]
                pdir = self._parent_dir(path, pattern)
                self.logger().info("Parent dir: %s -> %s" % (pattern, pdir))
                name_new = name_new.replace("{%s}" % pattern, pdir)

            self.logger().info("Result: %s -> %s" % (name, name_new))

            item_new = item.duplicate(source=os.path.join(path, name_new), name=name_new)
            result.append(item_new)

        return flatten_list(result)
