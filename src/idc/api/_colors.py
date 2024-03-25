from typing import List, Tuple
from PIL import ImageColor

# https://en.wikipedia.org/wiki/X11_color_names
X11_COLORS = [
    "#F0F8FF",
    "#FAEBD7",
    "#00FFFF",
    "#7FFFD4",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#000000",
    "#FFEBCD",
    "#0000FF",
    "#8A2BE2",
    "#A52A2A",
    "#DEB887",
    "#5F9EA0",
    "#7FFF00",
    "#D2691E",
    "#FF7F50",
    "#6495ED",
    "#FFF8DC",
    "#DC143C",
    "#00FFFF",
    "#00008B",
    "#008B8B",
    "#B8860B",
    "#A9A9A9",
    "#006400",
    "#BDB76B",
    "#8B008B",
    "#556B2F",
    "#FF8C00",
    "#9932CC",
    "#8B0000",
    "#E9967A",
    "#8FBC8F",
    "#483D8B",
    "#2F4F4F",
    "#00CED1",
    "#9400D3",
    "#FF1493",
    "#00BFFF",
    "#696969",
    "#1E90FF",
    "#B22222",
    "#FFFAF0",
    "#228B22",
    "#FF00FF",
    "#DCDCDC",
    "#F8F8FF",
    "#FFD700",
    "#DAA520",
    "#BEBEBE",
    "#808080",
    "#00FF00",
    "#008000",
    "#ADFF2F",
    "#F0FFF0",
    "#FF69B4",
    "#CD5C5C",
    "#4B0082",
    "#FFFFF0",
    "#F0E68C",
    "#E6E6FA",
    "#FFF0F5",
    "#7CFC00",
    "#FFFACD",
    "#ADD8E6",
    "#F08080",
    "#E0FFFF",
    "#FAFAD2",
    "#D3D3D3",
    "#90EE90",
    "#FFB6C1",
    "#FFA07A",
    "#20B2AA",
    "#87CEFA",
    "#778899",
    "#B0C4DE",
    "#FFFFE0",
    "#00FF00",
    "#32CD32",
    "#FAF0E6",
    "#FF00FF",
    "#B03060",
    "#800000",
    "#66CDAA",
    "#0000CD",
    "#BA55D3",
    "#9370DB",
    "#3CB371",
    "#7B68EE",
    "#00FA9A",
    "#48D1CC",
    "#C71585",
    "#191970",
    "#F5FFFA",
    "#FFE4E1",
    "#FFE4B5",
    "#FFDEAD",
    "#000080",
    "#FDF5E6",
    "#808000",
    "#6B8E23",
    "#FFA500",
    "#FF4500",
    "#DA70D6",
    "#EEE8AA",
    "#98FB98",
    "#AFEEEE",
    "#DB7093",
    "#FFEFD5",
    "#FFDAB9",
    "#CD853F",
    "#FFC0CB",
    "#DDA0DD",
    "#B0E0E6",
    "#A020F0",
    "#800080",
    "#663399",
    "#FF0000",
    "#BC8F8F",
    "#4169E1",
    "#8B4513",
    "#FA8072",
    "#F4A460",
    "#2E8B57",
    "#FFF5EE",
    "#A0522D",
    "#C0C0C0",
    "#87CEEB",
    "#6A5ACD",
    "#708090",
    "#FFFAFA",
    "#00FF7F",
    "#4682B4",
    "#D2B48C",
    "#008080",
    "#D8BFD8",
    "#FF6347",
    "#40E0D0",
    "#EE82EE",
    "#F5DEB3",
    "#FFFFFF",
    "#F5F5F5",
    "#FFFF00",
    "#9ACD32",
]

LIGHT_COLORS = [
    "#F0F8FF",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#FFEBCD",
    "#FFF8DC",
    "#FFFAF0",
    "#F8F8FF",
    "#F0FFF0",
    "#FFFFF0",
    "#FFF0F5",
    "#E0FFFF",
    "#FFFFE0",
    "#FAF0E6",
    "#F5FFFA",
    "#FDF5E6",
    "#FFF5EE",
    "#FFFAFA",
    "#FFFFFF",
    "#F5F5F5",
]

DARK_COLORS = [
    "#000000",
    "#00008B",
    "#191970",
    "#483D8B",
    "#2F4F4F",
    "#4B0082",
    "#191970",
    "#000080",
]


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


def default_colors(no_light=True, no_dark=True) -> List:
    """
    Returns a list of default color tuples.

    :param no_light: skips light colors
    :type no_light: bool
    :param no_dark: skips dark colors
    :type no_dark: bool
    :return: the nested list of colors
    :rtype: list
    """
    result = []
    skip = set()
    if no_light:
        for c in LIGHT_COLORS:
            skip.add(c)
    if no_dark:
        for c in DARK_COLORS:
            skip.add(c)
    for c in X11_COLORS:
        if c in skip:
            continue
        result.append(ImageColor.getrgb(c))
    return result


def text_color(color: Tuple[int, int, int], threshold=128) -> Tuple[int, int, int]:
    """
    Computes the text color to use for the given RGB color.

    :param color: the RGB tuple
    :param threshold: the threshold to use
    :return: the text color tuple
    :rtype: tuple
    """
    r, g, b = color
    if rgb2yiq(r, g, b) >= threshold:
        return 0, 0, 0
    else:
        return 255, 255, 255


def default_palette() -> List[int]:
    """
    Returns a palette of 255 R,G,B triplets all in a single list, to be used in indexed PNG files.

    :return: the flat list of R,G,B values
    :rtype: list
    """
    return [0, 0, 0,
            255, 0, 0,
            0, 255, 0] + [1 + i // 3 for i in range(759)]
