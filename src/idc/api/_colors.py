from typing import Tuple, List, Dict, Union
from simple_palette_utils import colors, x11_colors, COLOR_LISTS, COLOR_LIST_X11


def rgb2yiq(r: int, g: int, b: int) -> float:
    """
    Generates YIQ perceived brightness from RGB colors.

    :param r: the red value
    :type r: int
    :param g: the green value
    :type g: int
    :param b: the blue value
    :type b: int
    :return: the YIQ value
    :rtype: float
    """
    return ((r * 299) + (g * 587) + (b * 114)) / 1000


def text_color(color: Tuple[int, int, int], threshold: int = 128) -> Tuple[int, int, int]:
    """
    Computes the text color to use for the given RGB color.

    :param color: the RGB tuple (R/G/B)
    :type color: tuple
    :param threshold: the threshold to use
    :type threshold: int
    :return: the text color tuple (R/G/B)
    :rtype: tuple
    """
    r, g, b = color
    if rgb2yiq(r, g, b) >= threshold:
        return 0, 0, 0
    else:
        return 255, 255, 255
