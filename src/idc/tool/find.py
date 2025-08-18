import logging
import sys
import traceback

from wai.logging import init_logging, set_logging_level

from idc.core import ENV_IDC_LOGLEVEL
from kasperl.api import find_files_parser, find_files

FIND = "idc-find"

_logger = logging.getLogger(FIND)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    parser = find_files_parser("Tool for locating files in directories that match certain patterns and store them in files.", FIND)
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
