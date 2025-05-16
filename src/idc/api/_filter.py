import argparse
from seppl.io import Filter


APPLY_TO_IMAGE = "image"
APPLY_TO_ANNOTATIONS = "annotations"
APPLY_TO_BOTH = "both"
APPLY_TO = [
    APPLY_TO_BOTH,
    APPLY_TO_IMAGE,
    APPLY_TO_ANNOTATIONS
]


def add_apply_to_param(parser: argparse.ArgumentParser, default: str = APPLY_TO_IMAGE):
    """
    Adds the -a/--apply_to parameter to the parser.

    :param parser: the parser to add the option to
    :type parser: argparse.ArgumentParser
    :param default: the default value
    :type default: str
    """
    parser.add_argument("-a", "--apply_to", choices=APPLY_TO, help="Where to apply the filter to.",
                        default=default, required=False)


def parse_filter(filter_: str) -> Filter:
    """
    Parses the command-line and instantiates the filter.

    :param filter_: the command-line to parse
    :type filter_: str
    :return: the filter
    :rtype: Filter
    """
    from seppl import split_args, split_cmdline, args_to_objects
    from idc.registry import available_filters

    if filter_ is None:
        raise Exception("No filter command-line supplied!")
    valid = dict()
    valid.update(available_filters())
    args = split_args(split_cmdline(filter_), list(valid.keys()))
    objs = args_to_objects(args, valid, allow_global_options=False)
    if len(objs) == 1:
        if isinstance(objs[0], Filter):
            result = objs[0]
        else:
            raise Exception("Expected instance of Filter but got: %s" % str(type(objs[0])))
    else:
        raise Exception("Expected to obtain one filter from '%s' but got %d instead!" % (filter_, len(objs)))
    return result
