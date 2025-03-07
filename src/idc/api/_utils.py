import copy
import csv
import importlib
import inspect
import io
import logging
import numpy as np
import os
from typing import Optional, Union, List, Dict, Tuple, Callable, Any

from PIL import Image


def strip_suffix(path: str, suffix: str) -> str:
    """
    Removes the suffix from the file, if possible.

    :param path: the filename to process
    :type path: str
    :param suffix: the suffix to remove (including extension); ignored if None or ""
    :type suffix: str
    :return: the (potentially) updated filename
    :rtype: str
    """
    if suffix is not None:
        if len(suffix) == 0:
            suffix = None
    if suffix is not None:
        if path.endswith(suffix):
            return path[0:-len(suffix)]
    return path


def locate_file(path: str, ext: Union[str, List[str]], rel_path: str = None, suffix: str = None) -> List[str]:
    """
    Tries to locate the associate files for the given path by replacing its extension by the provided ones.

    :param path: the base path to use
    :type path: str
    :param ext: the extension(s) to look for (incl dot)
    :type ext: str or list
    :param suffix: the suffix to strip from the files, ignored if None or ""
    :type suffix: str
    :param rel_path: the relative path to the annotation to use for looking for associated files, ignored if None
    :type rel_path: str
    :return: the located files
    :rtype: list
    """
    result = []
    if rel_path is not None:
        parent_path = os.path.dirname(path)
        name = os.path.basename(path)
        path = os.path.join(parent_path, rel_path, name)
    path = strip_suffix(path, suffix)
    noext = os.path.splitext(path)[0]
    for current in ext:
        path = noext + current
        if os.path.exists(path):
            result.append(path)
    return result


def locate_image(path: str, rel_path: str = None, suffix: str = None) -> Optional[str]:
    """
    Tries to locate the image (png or jpg) for the given path by replacing its extension.

    :param path: the base path to use
    :type path: str
    :param rel_path: the relative path to the annotation to use for looking for images, ignored if None
    :type rel_path: str
    :param suffix: the suffix to strip from the files, ignored if None or ""
    :type suffix: str
    :return: the located image, None if not found
    :rtype: str
    """
    ext = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]
    images = locate_file(path, ext, rel_path=rel_path, suffix=suffix)
    if len(images) == 0:
        return None
    else:
        return images[0]


def load_image_from_bytes(data) -> Image:
    """
    Loads a Pillow image from the bytes.

    :param data: the bytes to load from
    :return: the image loaded from the data
    :rtype: Image
    """
    return Image.open(io.BytesIO(data))


def load_image_from_file(path: str) -> Image:
    """
    Loads a Pillow image from the specified file.

    :param path: the path to load from
    :return: the image loaded from the file
    :rtype: Image
    """
    return Image.open(path)


def load_labels(path: str, logger: logging.Logger = None) -> Tuple[List[str], Dict[int, str]]:
    """
    Loads the comma-separated labels from the text file and returns
    them as list and as index/label mapping.

    :param path: the file to load the labels from
    :type path: str
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    :return: the tuple of labels list and dictionary of index/label mapping
    :rtype: tuple
    """
    if logger is not None:
        logger.info("Reading labels from: %s" % str(path))
    with open(path, "r") as fp:
        line = fp.readline()
    labels = [x.strip() for x in line.strip().split(",")]
    label_mapping = dict()
    for i, label in enumerate(labels):
        label_mapping[i] = label
    if logger is not None:
        logger.debug("label mapping: %s" % str(label_mapping))
    return labels, label_mapping


def save_labels(path: str, labels: List[str], logger: logging.Logger = None):
    """
    Writes the labels as comma-separated list to the specified file.

    :param path: the file to write the labels to
    :type path: str
    :param labels: the labels to write
    :type labels: list
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    """
    if logger is not None:
        logger.info("Writing labels file: %s" % path)
    with open(path, "w") as fp:
        fp.write(",".join(labels))


def save_labels_csv(path: str, labels: Dict[int, str], logger: logging.Logger = None):
    """
    Writes the labels as CSV (Index,Label) to the specified file.

    :param path: the file to write the labels to
    :type path:
    :param labels:
    :param logger:
    :return:
    """
    if logger is not None:
        logger.info("Writing labels CSV file: %s" % path)

    rows = [["Index", "Label"]]
    for key in labels:
        rows.append([labels[key], key])
    with open(path, "w") as fp:
        writer = csv.writer(fp)
        writer.writerows(rows)


def load_function(function: str) -> Callable:
    """
    Parses the function definition and returns the function.
    The default format is "module_name:function_name".
    Raises exceptions if wrong format, missing or not an actual function.

    :param function: the function definition to parse
    :type function: str
    :return: the parsed function
    """
    if ":" not in function:
        raise Exception("Expected format 'module_name:function_name' but got: %s" % function)
    else:
        module_name, func_name = function.split(":")

    try:
        module = importlib.import_module(module_name)
    except:
        raise Exception("Failed to import class lister module: %s" % module_name)

    if hasattr(module, func_name):
        func = getattr(module, func_name)
        if inspect.isfunction(func):
            return func
        else:
            raise Exception("Not an actual function: %s" % function)
    else:
        raise Exception("Function '%s' not found in module '%s'!" % (func_name, module_name))


def pad_image(img: Union[Image.Image, np.ndarray], pad_width: Optional[int] = None, pad_height: Optional[int] = None) -> Image:
    """
    Pads the image/layer if necessary (on the right/bottom).

    :param img: the image to pad
    :type img: Image.Image/np.ndarray
    :param pad_width: the width to pad to, return as is if None
    :type pad_width: int
    :param pad_height: the height to pad to, return as is if None
    :type pad_height: int
    :return: the (potentially) padded image
    :rtype: Image.Image/np.ndarray
    """
    result = img
    if isinstance(img, Image.Image):
        width, height = img.size
    else:
        height = img.shape[0]
        width = img.shape[1]
    pad = False

    if (pad_width is not None) and (pad_height is not None):
        pad = (width != pad_width) or (height != pad_height)
    elif pad_width is not None:
        pad = width != pad_width
        pad_height = height
    elif pad_height is not None:
        pad = height != pad_height
        pad_width = width

    if pad:
        if isinstance(img, Image.Image):
            result = Image.new(img.mode, (pad_width, pad_height))
            result.paste(img)
        else:
            result = np.zeros((pad_height, pad_width), dtype=img.dtype)
            result[0:height, 0:width] = img

    return result


def crop_image(img: Union[Image.Image, np.ndarray], crop_width: Optional[int] = None, crop_height: Optional[int] = None) -> Image:
    """
    Crops the image/layer if necessary (removes on the right/bottom).

    :param img: the image to pad
    :type img: Image.Image/np.ndarray
    :param crop_width: the width to crop to, return as is if None
    :type crop_width: int
    :param crop_height: the height to crop to, return as is if None
    :type crop_height: int
    :return: the (potentially) cropped image
    :rtype: Image.Image/np.ndarray
    """
    result = img
    if isinstance(img, Image.Image):
        width, height = img.size
    else:
        height = img.shape[0]
        width = img.shape[1]
    crop = False

    if (crop_width is not None) and (crop_height is not None):
        crop = (width != crop_width) or (height != crop_height)
    elif crop_width is not None:
        crop = width != crop_width
        crop_height = height
    elif crop_height is not None:
        crop = height != crop_height
        crop_width = width

    if crop:
        if isinstance(img, Image.Image):
            result = img.crop((0, 0, crop_width, crop_height))
        else:
            result = img[0:crop_height, 0:crop_width]

    return result


def safe_deepcopy(obj: Optional[Any]) -> Optional[Any]:
    """
    Creates a deep copy of the object. Skips None objects.

    :param obj: the object to copy, can be None
    :return: the copy or None
    """
    if obj is None:
        return None
    else:
        return copy.deepcopy(obj)
