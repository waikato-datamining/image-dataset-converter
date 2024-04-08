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


# Taken from here:
# http://mkweb.bcgsc.ca/colorblind/palettes.mhtml
# http://mkweb.bcgsc.ca/colorblind/palettes/8.color.blindness.palette.txt
COLORBLIND8_COLORS = [
    "#000000",
    "#2271B2",
    "#3DB7E9",
    "#F748A5",
    "#359B73",
    "#d55e00",
    "#e69f00",
    "#f0e442",
]


# Taken from here:
# http://mkweb.bcgsc.ca/colorblind/palettes.mhtml
# http://mkweb.bcgsc.ca/colorblind/palettes/12.color.blindness.palette.txt
COLORBLIND12_COLORS = [
    "#9F0162",
    "#009F81",
    "#FF5AAF",
    "#00FCCF",
    "#8400CD",
    "#008DF9",
    "#00C2F9",
    "#FFB2FD",
    "#A40122",
    "#E20134",
    "#FF6E3A",
    "#FFC33B",
]


# Taken from here:
# http://mkweb.bcgsc.ca/colorblind/palettes.mhtml
# http://mkweb.bcgsc.ca/colorblind/palettes/15.color.blindness.palette.txt
COLORBLIND15_COLORS = [
    "#68023F",
    "#008169",
    "#EF0096",
    "#00DCB5",
    "#FFCFE2",
    "#003C86",
    "#9400E6",
    "#009FFA",
    "#FF71FD",
    "#7CFFFA",
    "#6A0213",
    "#008607",
    "#F60239",
    "#00E307",
    "#FFDC3D",
]


# Taken from here:
# http://mkweb.bcgsc.ca/colorblind/palettes.mhtml
# http://mkweb.bcgsc.ca/colorblind/palettes/24.color.blindness.palette.txt
COLORBLIND24_COLORS = [
    "#003D30",
    "#005745",
    "#00735C",
    "#009175",
    "#00AF8E",
    "#00CBA7",
    "#00EBC1",
    "#86FFDE",
    "#00306F",
    "#00489E",
    "#005FCC",
    "#0079FA",
    "#009FFA",
    "#00C2F9",
    "#00E5F8",
    "#7CFFFA",
    "#004002",
    "#005A01",
    "#007702",
    "#009503",
    "#00B408",
    "#00D302",
    "#00F407",
    "#AFFF2A",
]


PALETTE_AUTO = "auto"
PALETTE_GRAYSCALE = "grayscale"
PALETTE_X11 = "x11"
PALETTE_LIGHT = "light"
PALETTE_DARK = "dark"
PALETTE_COLORBLIND8 = "colorblind8"
PALETTE_COLORBLIND12 = "colorblind12"
PALETTE_COLORBLIND15 = "colorblind15"
PALETTE_COLORBLIND24 = "colorblind24"
PALETTES = [
    PALETTE_AUTO,
    PALETTE_GRAYSCALE,
    PALETTE_X11,
    PALETTE_LIGHT,
    PALETTE_DARK,
    PALETTE_COLORBLIND8,
    PALETTE_COLORBLIND12,
    PALETTE_COLORBLIND15,
    PALETTE_COLORBLIND24,
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


def create_palette(num_colors: int) -> List[int]:
    """
    Returns a list of palette entries (R,G,B) with the specified number of colors.

    :param num_colors: the number of colors to generate
    :type num_colors: int
    :return: the generated list of colors
    :rtype: list
    """
    return [1 + i // 3 for i in range(3*num_colors)]


def fill_palette(palette: List[int]) -> List[int]:
    """
    Makes sure that there are 256 R,G,B values present. Simply adds grayscale R,G,B values.

    :param palette: the palette to fill up, if necessary
    :type palette: list
    :return: the (potentially) updated list of R,G,B values
    :rtype: list
    """
    if len(palette) < 256*3:
        if len(palette) % 3 != 0:
            raise ValueError("Palette does not contain multiples of three (ie R,G,B values)!")
        palette = palette + create_palette(256 - (len(palette) // 3))
    return palette


def default_palette(palette: str = None) -> List[int]:
    """
    Returns a palette of 255 R,G,B triplets all in a single list, to be used in indexed PNG files.
    Black is always the first color.

    :return: the flat list of R,G,B values
    :rtype: list
    """
    if palette is None:
        palette = PALETTE_AUTO
    if palette not in PALETTES:
        raise ValueError("Unknown palette: %s" % palette)
    if palette == PALETTE_AUTO:
        result = [0, 0, 0,      # black
                  255, 0, 0,    # red
                  0, 255, 0,    # green
                  0, 0, 255,    # blue
                  255, 0, 255,  # magenta
                  255, 255, 0,  # yellow
                  0, 255, 255]  # cyan
    elif palette == PALETTE_GRAYSCALE:
        result = [0, 0, 0]
    elif palette == PALETTE_X11:
        result = [0, 0, 0]
        for c in X11_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_LIGHT:
        result = [0, 0, 0]
        for c in LIGHT_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_DARK:
        result = [0, 0, 0]
        for c in DARK_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_COLORBLIND8:
        result = [0, 0, 0]
        for c in COLORBLIND8_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_COLORBLIND12:
        result = [0, 0, 0]
        for c in COLORBLIND12_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_COLORBLIND15:
        result = [0, 0, 0]
        for c in COLORBLIND15_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    elif palette == PALETTE_COLORBLIND24:
        result = [0, 0, 0]
        for c in COLORBLIND24_COLORS:
            if c == "#000000":
                continue
            result.extend(ImageColor.getrgb(c))
    else:
        raise Exception("Unhandled palette: %s" % palette)

    result = fill_palette(result)
    return result
