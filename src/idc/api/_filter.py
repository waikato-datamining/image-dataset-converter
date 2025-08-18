import argparse


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
