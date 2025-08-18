import logging
import traceback

from idc.core import ENV_IDC_LOGLEVEL
from idc.registry import available_generators
from kasperl.api import perform_generator_test

TEST_GENERATOR = "idc-test-generator"

_logger = logging.getLogger(TEST_GENERATOR)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    perform_generator_test(ENV_IDC_LOGLEVEL, args, TEST_GENERATOR, None, available_generators(), _logger)


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
        return 1


if __name__ == '__main__':
    main()
