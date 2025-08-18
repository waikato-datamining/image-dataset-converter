import logging

from kasperl.api import Session as KSession


ENV_IDC_LOGLEVEL = "IDC_LOGLEVEL"
""" environment variable for the global default logging level. """


class Session(KSession):
    """
    Session object shared among reader, filter(s), writer.
    """
    logger: logging.Logger = logging.getLogger("image-dataset-converter")
    """ the global logger. """
