import logging
import sys
import traceback

from idc.core import ENV_IDC_LOGLEVEL
from kasperl.api import perform_find_files

FIND = "idc-find"

_logger = logging.getLogger(FIND)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    perform_find_files(ENV_IDC_LOGLEVEL, args, FIND, None, _logger)


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
