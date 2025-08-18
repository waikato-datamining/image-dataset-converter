import traceback

from idc.core import ENV_IDC_LOGLEVEL
from idc.help import generate_plugin_usage
from idc.registry import available_readers, available_filters, available_writers
from kasperl.api import perform_conversion

CONVERT = "idc-convert"
DESCRIPTION = "Tool for converting between image annotation dataset formats."


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    perform_conversion(
        ENV_IDC_LOGLEVEL, args, CONVERT, DESCRIPTION,
        available_readers(), available_filters(), available_writers(),
        require_reader=True, require_writer=False, generate_plugin_usage=generate_plugin_usage)


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
