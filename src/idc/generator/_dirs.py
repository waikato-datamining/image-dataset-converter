import argparse
import os
import re
import traceback
from typing import Optional, List, Dict, Tuple

from wai.logging import LOGGING_WARNING
from idc.api import Generator


VAR_ABSDIR = "absdir"
VAR_RELDIR = "reldir"
VAR_DIRNAME = "dirname"
VARS = [
    VAR_ABSDIR,
    VAR_RELDIR,
    VAR_DIRNAME,
]


class DirectoryGenerator(Generator):
    """
    Iterates over directories that it finds.
    """

    def __init__(self, path: str = None, recursive: bool = False, regexp: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the generator.

        :param path: the path to search for directories
        :type path: str
        :param recursive: whether to search recursively
        :type recursive: bool
        :param regexp: the regular expression for matching directories
        :type regexp: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.path = path
        self.recursive = recursive
        self.regexp = regexp

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "dirs"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Iterates over directories that it finds. " \
            + "Available variables: " + "|".join(VARS) + ". " \
            + VAR_ABSDIR + ": the absolute directory, " \
            + VAR_RELDIR + ": the relative directory to the search path, " \
            + VAR_DIRNAME + ": the directory name (no parent path)."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-p", "--path", type=str, metavar="DIR", default=None, help="The directory/directories to serarch", required=True, nargs="+")
        parser.add_argument("-r", "--recursive", action="store_true", help="Whether to search for directories recursively.", required=False)
        parser.add_argument("--regexp", type=str, metavar="REGEXP", default=None, help="The regular expression to use for matching directories; matches all if not provided.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.path = ns.path
        self.recursive = ns.recursive
        self.regexp = ns.regexp

    def _check(self) -> Optional[str]:
        """
        Hook method for performing checks.

        :return: None if checks successful, otherwise error message
        :rtype: str
        """
        result = super()._check()

        if result is None:
            if self.regexp == "":
                self.regexp = None
            if self.regexp is not None:
                try:
                    re.compile(self.regexp)
                except:
                    result = "Invalid regular expression: %s\n%s" % (self.regexp, traceback.format_exc())

        if result is None:
            for p in self.path:
                if not os.path.exists(p):
                    result = "Directory does not exist: %s" % p
                elif not os.path.isdir(p):
                    result = "Not a directory: %s" % p

        return result

    def _locate(self, start: str, current: str, recursive: bool, paths: List[Tuple[str, str]]):
        """
        Locates directories.

        :param start: the starting directory (for determining relative dirs)
        :type start: str
        :param current: the directory to search
        :type current: str
        :param recursive: whether to search recursively
        :type recursive: bool
        :param paths: for collecting the matching dirs
        :type paths: list
        """
        for f in os.listdir(current):
            full = os.path.join(current, f)
            if os.path.isdir(full):
                if self.regexp is not None:
                    m = re.match(self.regexp, f)
                    if m is not None:
                        paths.append((start, full))
                else:
                    paths.append((start, full))
                if recursive:
                    self._locate(start, full, recursive, paths)

    def _do_generate(self) -> List[Dict[str, str]]:
        """
        Generates the variables.

        :return: the list of variable dictionaries
        :rtype: list
        """
        result = []

        # locate dirs
        paths = []
        for abs_dir in self.path:
            self._locate(os.path.abspath(abs_dir), os.path.abspath(abs_dir), self.recursive, paths)

        # prepare variables
        for parent_dir, abs_dir in paths:
            if abs_dir.startswith(parent_dir):
                rel_dir = abs_dir[len(parent_dir):]
                if rel_dir.startswith("/") or rel_dir.startswith("\\"):
                    rel_dir = rel_dir[1:]
            else:
                rel_dir = None
            dir_name = os.path.basename(abs_dir)
            result.append({
                VAR_ABSDIR: abs_dir,
                VAR_RELDIR: rel_dir,
                VAR_DIRNAME: dir_name,
            })

        return result
