import argparse
import logging
import traceback

from wai.logging import init_logging, set_logging_level, add_logging_level

from idc.api import Generator
from idc.core import ENV_IDC_LOGLEVEL
from idc.registry import available_generators

TEST_GENERATOR = "idc-test-generator"

_logger = logging.getLogger(TEST_GENERATOR)


def test_generator(generator: str):
    """
    Parses/executes the generator and then outputs the generated variables.

    :param generator: the generator command-line to use for generating variable values
    :type generator: str
    """
    # parse generator
    generator_obj = Generator.parse_generator(generator)

    # apply generator to pipeline template and execute it
    vars_list = generator_obj.generate()
    for vars_ in vars_list:
        print(vars_)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    generators = sorted(list(available_generators().keys()))
    parser = argparse.ArgumentParser(
        description="Tool for testing generators by outputting the generated variables and their associated values. Available generators: " + ", ".join(generators),
        prog=TEST_GENERATOR,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-g", "--generator", help="The generator plugin to use.", default=None, type=str, required=True)
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    test_generator(parsed.generator)


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
