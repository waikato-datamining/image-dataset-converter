import argparse
import logging
import os.path
import sys
import traceback

from typing import List, Tuple, Optional, Dict

from seppl import enumerate_plugins, is_help_requested, split_args, args_to_objects, Plugin, check_compatibility
from seppl.placeholders import load_user_defined_placeholders, expand_placeholders
from seppl.io import execute, Reader, Filter, MultiFilter, Writer
from wai.logging import init_logging, set_logging_level, add_logging_level, LOGGING_LEVELS

from idc.core import Session, ENV_IDC_LOGLEVEL
from idc.help import generate_plugin_usage
from idc.registry import available_readers, available_filters, available_writers, REGISTRY


CONVERT = "idc-convert"


DEFAULT_UPDATE_INTERVAL = 1000


def _available_plugins() -> Dict[str, Plugin]:
    """
    Returns the available reader/filter/writer plugins.

    :return: the dictionary of plugins (name/Plugin)
    :rtype: dict
    """
    result = dict()
    result.update(available_readers())
    result.update(available_filters())
    result.update(available_writers())
    return result


def _print_usage(plugin_details: bool = False):
    """
    Prints the program usage to stdout.
    Ensure global options are in sync with parser in parse_args method below.

    :param plugin_details: whether to output the plugin details as well
    :type plugin_details: bool
    """
    cmd = "usage: " + CONVERT
    prefix = " " * (len(cmd) + 1)
    logging_levels = ",".join(LOGGING_LEVELS)
    print(cmd + " [-h|--help|--help-all|--help-plugin NAME]")
    print(prefix + "[-u INTERVAL] [-b|--force_batch] [--placeholders FILE] [--dump_pipeline FILE]")
    print(prefix + "[-l {%s}]" % logging_levels)
    print(prefix + "reader")
    print(prefix + "[filter [filter [...]]]")
    print(prefix + "[writer]")
    print()
    print("Tool for converting between image annotation dataset formats.")
    print()
    print("readers (%d):\n" % len(available_readers()) + enumerate_plugins(available_readers().keys(), aliases=REGISTRY.all_aliases, prefix="   "))
    print("filters (%d):\n" % len(available_filters()) + enumerate_plugins(available_filters().keys(), aliases=REGISTRY.all_aliases, prefix="   "))
    print("writers (%d):\n" % len(available_writers()) + enumerate_plugins(available_writers().keys(), aliases=REGISTRY.all_aliases, prefix="   "))
    print()
    print("optional arguments:")
    print("  -h, --help            show basic help message and exit")
    print("  --help-all            show basic help message plus help on all plugins and exit")
    print("  --help-plugin NAME    show help message for plugin NAME and exit")
    print("  -u INTERVAL, --update_interval INTERVAL")
    print("                        outputs the progress every INTERVAL records (default: %d)" % DEFAULT_UPDATE_INTERVAL)
    print("  -l {%s}, --logging_level {%s}" % (logging_levels, logging_levels))
    print("                        the logging level to use (default: WARN)")
    print("  -b, --force_batch     processes the data in batches")
    print("  --placeholders FILE")
    print("                        The file with custom placeholders to load (format: key=value).")
    print("  --dump_pipeline FILE")
    print("                        The file to dump the pipeline command in.")
    print()
    if plugin_details:
        for plugin in sorted(_available_plugins().keys()):
            generate_plugin_usage(plugin)


def _parse_args(args: List[str], require_reader: bool = True, require_writer: bool = True) -> Tuple[Optional[Reader], Optional[Filter], Optional[Writer], Session]:
    """
    Parses the arguments.

    :param args: the arguments to parse
    :type args: list
    :param require_reader: whether a reader is required
    :type require_reader: bool
    :param require_writer: whether a writer is required
    :type require_writer: bool
    :return: tuple of (reader, filter, writer, session), the filter can be None
    :rtype: tuple
    """
    partial = False
    all_plugins = _available_plugins()
    handlers = list(all_plugins.keys())

    # help requested?
    help_requested, plugin_details, plugin_name = is_help_requested(args, handlers=handlers, partial=partial)
    if help_requested:
        if plugin_name is not None:
            generate_plugin_usage(plugin_name)
        else:
            _print_usage(plugin_details=plugin_details)
        sys.exit(0)

    parsed = split_args(args, handlers, partial=partial)
    plugins = args_to_objects(parsed, all_plugins, allow_global_options=True)
    reader = None
    writer = None
    filters = []
    for plugin in plugins:
        if isinstance(plugin, Reader):
            if reader is None:
                reader = plugin
                continue
            else:
                raise Exception("Only one reader can be defined!")

        if isinstance(plugin, Filter):
            filters.append(plugin)
            continue

        if isinstance(plugin, Writer):
            if writer is None:
                writer = plugin
                continue
            else:
                raise Exception("Only one writer can be defined!")

        raise Exception("Unhandled plugin type: %s" % str(type(plugin)))

    # checks whether valid pipeline
    if (reader is None) and require_reader:
        raise Exception("No reader defined!")
    if (writer is None) and require_writer:
        raise Exception("No writer defined!")
    if len(filters) == 0:
        filter_ = None
    elif len(filters) == 1:
        filter_ = filters[0]
    else:
        filter_ = MultiFilter(filters=filters)

    # check compatibility
    if writer is not None:
        if filter_ is not None:
            check_compatibility([reader, filter_, writer])
        else:
            check_compatibility([reader, writer])

    # global options?
    # see print_usage() method above
    parser = argparse.ArgumentParser()
    add_logging_level(parser)
    parser.add_argument("-u", "--update_interval", type=int, default=DEFAULT_UPDATE_INTERVAL)
    parser.add_argument("-b", "--force_batch", action="store_true")
    parser.add_argument("--placeholders")
    parser.add_argument("--dump_pipeline")
    session = Session(options=parser.parse_args(parsed[""] if ("" in parsed) else []))
    session.logger = logging.getLogger(CONVERT)
    set_logging_level(session.logger, session.options.logging_level)
    if session.options.placeholders is not None:
        if not os.path.exists(session.options.placeholders):
            session.logger.error("Placeholder file not found: %s" % session.options.placeholders)
        else:
            session.logger.info("Loading custom placeholders from: %s" % session.options.placeholders)
            load_user_defined_placeholders(session.options.placeholders)
    if session.options.dump_pipeline is not None:
        session.logger.info("Dumping pipeline command in: %s" % session.options.dump_pipeline)
        with open(expand_placeholders(session.options.dump_pipeline), "w") as fp:
            fp.write(CONVERT + "\n")
            fp.write("\n".join(args))

    return reader, filter_, writer, session


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_IDC_LOGLEVEL)
    _args = sys.argv[1:] if (args is None) else args
    try:
        reader, filter_, writer, session = _parse_args(_args, require_writer=False)
    except Exception:
        traceback.print_exc()
        print("options: %s" % str(_args), file=sys.stderr)
        _print_usage()
        sys.exit(1)

    session.logger.info("options: %s" % str(_args))

    execute(reader, filter_, writer, session)


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
