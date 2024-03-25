import traceback
from typing import Tuple

from matplotlib import font_manager
from PIL import ImageFont, Image, ImageDraw


DEFAULT_FONT_FAMILY = "sans\\-serif"

TEXT_SIZE_OLD = None


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


def _text_size_old(text: str, font) -> Tuple[int, int]:
    """
    Computes the width/height of a text using the specified Pillow font.
    Uses ImageDraw.textsize.

    :param text: the text to get the dimensions for
    :type text: str
    :param font: the Pillow font to use
    :return: the width and height
    :rtype: tuple
    """
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    w, h = draw.textsize(text, font=font)
    return w, h


def _text_size_new(text: str, font) -> Tuple[int, int]:
    """
    Computes the width/height of a text using the specified Pillow font.
    Newer versions of Pillow deprecated ImageDraw.textsize
    https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd

    :param text: the text to get the dimensions for
    :type text: str
    :param font: the Pillow font to use
    :return: the width and height
    :rtype: tuple
    """
    ascent, descent = font.getmetrics()
    w = font.getmask(text).getbbox()[2]
    h = font.getmask(text).getbbox()[3] + descent
    return w, h


def text_size(text: str, font) -> Tuple[int, int]:
    """
    Computes the width/height of a text using the specified Pillow font.

    :param text: the text to get the dimensions for
    :type text: str
    :param font: the Pillow font to use
    :return: the width and height
    :rtype: tuple
    """
    global TEXT_SIZE_OLD

    if TEXT_SIZE_OLD is None:
        try:
            w, h = _text_size_old(text, font)
            TEXT_SIZE_OLD = True
        except:
            w, h = _text_size_new(text, font)
            TEXT_SIZE_OLD = False
    else:
        if TEXT_SIZE_OLD:
            w, h = _text_size_old(text, font)
        else:
            w, h = _text_size_new(text, font)
    return w, h
