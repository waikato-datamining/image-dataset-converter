import argparse
import logging
import os
import traceback

from seppl import split_cmdline
from seppl.placeholders import load_user_defined_placeholders
from wai.logging import init_logging, set_logging_level, add_logging_level

from idc.api import Generator
from idc.core import ENV_IDC_LOGLEVEL
from idc.registry import available_generators
from idc.tool.convert import main as convert_main, CONVERT

EXEC = "idc-exec"

_logger = logging.getLogger(EXEC)


def execute_pipeline(pipeline: str, generator: str, dry_run: bool = False, prefix: str = False):
    """
    Executes the specified pipeline as many times as the generators produce variables.

    :param pipeline: the pipeline template to use
    :type pipeline: str
    :param generator: the generator command-line to use for generating variable values to be expanded in the pipeline template
    :type generator: str
    :param dry_run: whether to only expand/output but not execute the pipeline
    :type dry_run: bool
    :param prefix: the prefix to use when in dry-run mode
    :type prefix: str
    """
    # remove whitespaces, idc-convert from pipeline
    pipeline = pipeline.strip()
    if pipeline.startswith(CONVERT):
        pipeline = pipeline[len(CONVERT):].strip()

    # parse generator
    generator_obj = Generator.parse_generator(generator)

    # apply generator to pipeline template and execute it
    vars_list = generator_obj.generate()
    for vars_ in vars_list:
        pipeline_exp = pipeline
        for var in vars_:
            pipeline_exp = pipeline_exp.replace("{%s}" % var, vars_[var])
        _logger.info("%s\n--> %s" % (pipeline, pipeline_exp))
        if dry_run:
            if prefix is not None:
                if not prefix.endswith(" "):
                    prefix = prefix + " "
                pipeline_exp = prefix + pipeline_exp
            print(pipeline_exp)
        else:
            pipeline_args = split_cmdline(pipeline_exp)
            convert_main(pipeline_args)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    generators = sorted(list(available_generators().keys()))
    parser = argparse.ArgumentParser(
        description="Tool for executing a pipeline multiple times, each time with a different set of variables expanded. A variable is surrounded by curly quotes (e.g., variable 'i' gets referenced with '{i}'). Available generators: " + ", ".join(generators),
        prog=EXEC,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--pipeline", help="The pipeline template with variables to expand and then execute.", default=None, type=str, required=True)
    parser.add_argument("-g", "--generator", help="The generator plugin to use.", default=None, type=str, required=True)
    parser.add_argument("-n", "--dry_run", action="store_true", help="Applies the generator to the pipeline template and only outputs it on stdout.", required=False)
    parser.add_argument("-P", "--prefix", help="The string to prefix the pipeline with when in dry-run mode.", required=False, default=None, type=str)
    parser.add_argument("--placeholders", metavar="FILE", help="The file with custom placeholders to load (format: key=value).", required=False, default=None, type=str)
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    if parsed.placeholders is not None:
        if not os.path.exists(parsed.placeholders):
            _logger.error("Placeholder file not found: %s" % parsed.placeholders)
        else:
            _logger.info("Loading custom placeholders from: %s" % parsed.placeholders)
            load_user_defined_placeholders(parsed.placeholders)
    execute_pipeline(parsed.pipeline, parsed.generator,
                     dry_run=parsed.dry_run, prefix=parsed.prefix)


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
