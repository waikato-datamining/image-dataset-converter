import argparse
import logging
import sys
import traceback

from wai.logging import init_logging, set_logging_level, add_logging_level

from idc.core import ENV_IDC_LOGLEVEL
from kasperl.api import find_files

FIND = "idc-find"

_logger = logging.getLogger(FIND)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    parser = argparse.ArgumentParser(
        description="Tool for locating files in directories that match certain patterns and store them in files.",
        prog=FIND,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="DIR", help="The dir(s) to scan for files.", default=None, type=str, required=True, nargs="+")
    parser.add_argument("-r", "--recursive", action="store_true", help="Whether to search the directories recursively", required=False)
    parser.add_argument("-o", "--output", metavar="FILE", help="The file to store the located file names in", type=str, required=True)
    parser.add_argument("-m", "--match", metavar="REGEXP", help="The regular expression that the (full) file names must match to be included", default=None, type=str, required=False, nargs="*")
    parser.add_argument("-n", "--not-match", metavar="REGEXP", help="The regular expression that the (full) file names must match to be excluded", default=None, type=str, required=False, nargs="*")
    parser.add_argument("--split_ratios", type=int, default=None, help="The split ratios to use for generating the splits (int; must sum up to 100)", nargs="*")
    parser.add_argument("--split_names", type=str, default=None, help="The split names to use as filename suffixes for the generated splits (before .ext)", nargs="*")
    parser.add_argument("--split_name_separator", type=str, default="-", help="The separator to use between file name and split name", required=False)
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    find_files(parsed.input, parsed.output, recursive=parsed.recursive,
               match=parsed.match, not_match=parsed.not_match,
               split_ratios=parsed.split_ratios, split_names=parsed.split_names,
               split_name_separator=parsed.split_name_separator, logger=_logger)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        print("options: %s" % str(sys.argv[1:]), file=sys.stderr)
        return 1


if __name__ == '__main__':
    main()
