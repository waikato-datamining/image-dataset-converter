import argparse
import logging
import os
import traceback

from typing import Dict, List, Optional

from seppl import ClassListerRegistry, Plugin, get_class_name

# environment variable with comma-separated list of class listers to use
ENV_IDC_CLASS_LISTERS = "IDC_CLASS_LISTERS"

# environment variable with comma-separated list of class listers to exclude
ENV_IDC_CLASS_LISTERS_EXCL = "IDC_CLASS_LISTERS_EXCL"

# the default class listers to inspect (for development)
# can be overridden with IDC_CLASS_LISTERS environment variable
DEFAULT_IDC_CLASS_LISTERS = [
    "idc.class_lister",
]

REGISTRY = ClassListerRegistry(default_class_listers=DEFAULT_IDC_CLASS_LISTERS,
                               env_class_listers=ENV_IDC_CLASS_LISTERS,
                               env_excluded_class_listers=ENV_IDC_CLASS_LISTERS_EXCL)

IMG_REGISTRY = "idc-registry"

_logger = None


LIST_PLUGINS = "plugins"
LIST_PIPELINE = "pipeline"
LIST_READERS = "readers"
LIST_FILTERS = "filters"
LIST_WRITERS = "writers"
LIST_GENERATORS = "generators"
LIST_CUSTOM_CLASS_LISTERS = "custom-class-listers"
LIST_ENV_CLASS_LISTERS = "env-class-listers"
LIST_TYPES = [
    LIST_PLUGINS,
    LIST_PIPELINE,
    LIST_CUSTOM_CLASS_LISTERS,
    LIST_ENV_CLASS_LISTERS,
    LIST_READERS,
    LIST_FILTERS,
    LIST_WRITERS,
    LIST_GENERATORS,
]


def logger() -> logging.Logger:
    """
    Returns the logger instance to use, initializes it if necessary.

    :return: the logger instance
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger(IMG_REGISTRY)
    return _logger


def available_readers() -> Dict[str, Plugin]:
    """
    Returns all available readers.

    :return: the dict of reader objects
    :rtype: dict
    """
    return REGISTRY.plugins("seppl.io.Reader", fail_if_empty=False)


def available_writers() -> Dict[str, Plugin]:
    """
    Returns all available writers.

    :return: the dict of writer objects
    :rtype: dict
    """
    return REGISTRY.plugins("seppl.io.Writer", fail_if_empty=False)


def available_filters() -> Dict[str, Plugin]:
    """
    Returns all available filters.

    :return: the dict of filter objects
    :rtype: dict
    """
    return REGISTRY.plugins("seppl.io.Filter", fail_if_empty=False)


def available_pipeline_plugins() -> Dict[str, Plugin]:
    """
    Returns all available plugins for building pipelines.

    :return: the dict of plugin objects
    :rtype: dict
    """
    result = dict()
    result.update(available_readers())
    result.update(available_filters())
    result.update(available_writers())
    return result


def available_generators() -> Dict[str, Plugin]:
    """
    Returns all available generators.

    :return: the dict of generator objects
    :rtype: dict
    """
    return REGISTRY.plugins("idc.api.Generator", fail_if_empty=False)


def available_plugins() -> Dict[str, Plugin]:
    """
    Returns all available plugins (pipeline and generators).

    :return: the dict of plugin objects
    :rtype: dict
    """
    result = dict()
    result.update(available_readers())
    result.update(available_filters())
    result.update(available_writers())
    result.update(available_generators())
    return result


def register_plugins(custom_class_listers: List[str] = None, excluded_class_listers: List[str] = None):
    """
    Registers all plugins.

    :param custom_class_listers: the list of custom class listers to use instead of env variable or default class listers
    :type custom_class_listers: list
    :param excluded_class_listers: the list of class listers to exclude
    :type excluded_class_listers: list
    """
    REGISTRY.custom_class_listers = custom_class_listers
    REGISTRY.excluded_class_listers = excluded_class_listers
    available_plugins()


def _list(list_type: str, custom_class_listers: Optional[List[str]] = None, excluded_class_listers: Optional[List[str]] = None):
    """
    Lists various things on stdout.

    :param custom_class_listers: the list of custom class listers to use instead of env variable or default class listers
    :type custom_class_listers: list
    :param excluded_class_listers: the list of class listers to exclude
    :type excluded_class_listers: list
    :param list_type: the type of list to generate
    :type list_type: str
    """
    register_plugins(custom_class_listers=custom_class_listers, excluded_class_listers=excluded_class_listers)

    if list_type in [LIST_PLUGINS, LIST_PIPELINE, LIST_READERS, LIST_FILTERS, LIST_WRITERS, LIST_GENERATORS]:
        if list_type == LIST_PLUGINS:
            plugins = available_plugins()
        elif list_type == LIST_PIPELINE:
            plugins = available_pipeline_plugins()
        elif list_type == LIST_READERS:
            plugins = available_readers()
        elif list_type == LIST_FILTERS:
            plugins = available_filters()
        elif list_type == LIST_WRITERS:
            plugins = available_readers()
        elif list_type == LIST_GENERATORS:
            plugins = available_generators()
        else:
            raise Exception("Unhandled type: %s" % list_type)
        print("name: class")
        for name in plugins:
            print("%s: %s" % (name, get_class_name(plugins[name])))
    elif list_type == LIST_CUSTOM_CLASS_LISTERS:
        class_listers = REGISTRY.custom_class_listers
        print("custom class listers:")
        if class_listers is None:
            print("-none")
        else:
            for m in class_listers:
                print(m)
    elif list_type == LIST_ENV_CLASS_LISTERS:
        print("env class listers:")
        if REGISTRY.env_class_listers is None:
            print("-none-")
        else:
            class_listers = os.getenv(REGISTRY.env_class_listers)
            if class_listers is None:
                print("-none listed in env var %s-" % REGISTRY.env_class_listers)
            else:
                class_listers = class_listers.split(",")
                for m in class_listers:
                    print(m)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="For inspecting/querying the registry.",
        prog=IMG_REGISTRY,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--custom_class_listers", type=str, default=None, help="The comma-separated list of custom class listers to use.", required=False)
    parser.add_argument("-e", "--excluded_class_listers", type=str, default=None, help="The comma-separated list of class listers to exclude.", required=False)
    parser.add_argument("-l", "--list", choices=LIST_TYPES, default=None, help="For outputting various lists on stdout.", required=False)
    parsed = parser.parse_args(args=args)

    custom_class_listers = None
    if parsed.custom_class_listers is not None:
        custom_class_listers = parsed.custom_class_listers.split(",")

    if parsed.list is not None:
        _list(parsed.list, custom_class_listers=custom_class_listers)


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
