import logging

import seppl


ENV_IDC_LOGLEVEL = "IDC_LOGLEVEL"
""" environment variable for the global default logging level. """


class Session(seppl.Session):
    """
    Session object shared among reader, filter(s), writer.
    """
    logger: logging.Logger = logging.getLogger("img-dataset-converter")
    """ the global logger. """
