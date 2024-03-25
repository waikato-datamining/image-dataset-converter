import traceback

from matplotlib import font_manager
from PIL import ImageFont


DEFAULT_FONT_FAMILY = "sans\\-serif"


def load_font(logger, family, size):
    """
    Attempts to instantiate the specified font family.

    :param logger: the logger instance to use, ignored if None
    :param family: the TTF font family
    :type family: str
    :param size: the size to use
    :type size: int
    :return: the Pillow font
    """
    try:
        mpl_font = font_manager.FontProperties(family=family)
        font_file = font_manager.findfont(mpl_font)
        return ImageFont.truetype(font_file, size)
    except:
        msg = "Failed to instantiate font family '%s', falling back on '%s'" % (family, DEFAULT_FONT_FAMILY)
        if logger is not None:
            logger.warning(msg, exc_info=True)
        else:
            print(msg)
            print(traceback.format_exc())

        mpl_font = font_manager.FontProperties(family=DEFAULT_FONT_FAMILY)
        font_file = font_manager.findfont(mpl_font)
        return ImageFont.truetype(font_file, size)
