import csv
import io
import logging
import os
from typing import Optional, Union, List, Dict, Tuple

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
