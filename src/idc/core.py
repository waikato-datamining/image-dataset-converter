import logging

import seppl


ENV_IDC_LOGLEVEL = "IDC_LOGLEVEL"
""" environment variable for the global default logging level. """


COMPARISON_LESSTHAN = "lt"
COMPARISON_LESSOREQUAL = "le"
COMPARISON_EQUAL = "eq"
COMPARISON_NOTEQUAL = "ne"
COMPARISON_GREATEROREQUAL = "ge"
COMPARISON_GREATERTHAN = "gt"
COMPARISON_CONTAINS = "contains"
COMPARISON_MATCHES = "matches"

COMPARISONS = [
    COMPARISON_LESSTHAN,
    COMPARISON_LESSOREQUAL,
    COMPARISON_EQUAL,
    COMPARISON_NOTEQUAL,
    COMPARISON_GREATEROREQUAL,
    COMPARISON_GREATERTHAN,
]
COMPARISON_HELP = COMPARISON_LESSTHAN + ": less than, " \
    + COMPARISON_LESSOREQUAL + ": less or equal, " \
    + COMPARISON_EQUAL + ": equal, " \
    + COMPARISON_NOTEQUAL + ": not equal, " \
    + COMPARISON_GREATERTHAN + ": greater than, " \
    + COMPARISON_GREATEROREQUAL + ": greater of equal"

COMPARISONS_EXT = COMPARISONS[:]
COMPARISONS_EXT.append(COMPARISON_CONTAINS)
COMPARISONS_EXT.append(COMPARISON_MATCHES)
COMPARISON_EXT_HELP = COMPARISON_HELP + ", " \
                      + COMPARISON_CONTAINS + ": substring match, " \
                      + COMPARISON_MATCHES + ": regexp match"


class Session(seppl.Session):
    """
    Session object shared among reader, filter(s), writer.
    """
    logger: logging.Logger = logging.getLogger("image-dataset-converter")
    """ the global logger. """
