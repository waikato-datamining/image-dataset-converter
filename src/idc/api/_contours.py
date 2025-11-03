import logging

import cv2
import numpy as np
from PIL import Image
from shapely import Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects
from ._geometry import shapely_to_locatedobject

MIN_RECT_WIDTH = "min_rect_width"
MIN_RECT_HEIGHT = "min_rect_height"


def _check_dimension(dim, min_size: int = None, max_size: int = None) -> bool:
    """
    Checks whether the dimension fits the min/max size.

    :param dim: the width/height to check
    :type dim: int
    :param min_size: the minimum size
    :type min_size: int or None
    :param max_size: the maximum size
    :type max_size: int or None
    :return: True if within specified min/max
    :rtype: bool
    """
    if min_size is not None:
        if dim < min_size:
            return False
    if max_size is not None:
        if dim > max_size:
            return False
    return True


def contours_to_objdet(contours, ann: LocatedObjects, label: str, min_size: int = None, max_size: int = None,
                       calculate_min_rect: bool = False):
    """
    Processes the contours and adds the polygons to the annotations.

    :param contours: the contours to process
    :param ann: the annotations to append
    :type ann: LocatedObjects
    :param label: the label to use
    :type label: str
    :param min_size: the minimum size (width and height) that a contour must have
    :type min_size: int
    :param max_size: the maximum size (width and height) that a contour can have
    :type max_size: int
    :param calculate_min_rect: whether to calculate the min_rect width/height as well
    :type calculate_min_rect: bool
    """
    for i in range(len(contours)):
        if len(contours[i]) > 2:
            polygon = Polygon(np.squeeze(contours[i]))
            # Convert invalid polygon to valid
            if not polygon.is_valid:
                polygon = polygon.buffer(0)
            if polygon.area == 0.0:
                continue
            lobj = shapely_to_locatedobject(polygon, label=label)
            if min_size is not None:
                if not _check_dimension(lobj.width) or not _check_dimension(lobj.height, min_size=min_size, max_size=max_size):
                    continue
            if max_size is not None:
                if not _check_dimension(lobj.width) or not _check_dimension(lobj.height, min_size=min_size, max_size=max_size):
                    continue
            if calculate_min_rect:
                rect = cv2.minAreaRect(contours[i])
                (_, _), (w, h), angle = rect
                if not _check_dimension(w) or not _check_dimension(h):
                    continue
                lobj.metadata[MIN_RECT_WIDTH] = w
                lobj.metadata[MIN_RECT_HEIGHT] = h
            ann.append(lobj)


def objdet_from_instancepng(img: Image.Image, label: str, min_size: int = None, max_size: int = None,
                            logger: logging.Logger = None, background: int = 0) -> LocatedObjects:
    """
    Loads the annotations from the indexed png with instance annotations, i.e., each palette index
    represents a different object. For each of the layers all blobs get identified and turned
    into polygons.

    :param img: the image to turn into annotations
    :type img: Image.Image
    :param label: the label to use
    :type label: str
    :param min_size: the minimum size (width and height) that a contour must have
    :type min_size: int
    :param max_size: the maximum size (width and height) that a contour can have
    :type max_size: int
    :param logger: the (optional) logger for logging messages
    :type logger: logging.Logger
    :param background: the index (0-255) of the background, default 0
    :type background: int
    :return: the generated annotations
    :rtype: LocatedObjects
    """
    arr = np.asarray(img).astype(np.uint8)
    unique = np.unique(arr)
    result = LocatedObjects()
    for index in list(unique):
        # skip background
        if index == background:
            continue
        layer = np.where(arr == index, arr, 0)
        layer = np.where(layer > 0, 1, 0)
        contours, _ = cv2.findContours(np.array(layer).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if logger is not None:
            logger.info("%s - # of contours: %s" % (label, str(len(contours))))
        contours_to_objdet(contours, result, label, min_size=min_size, max_size=max_size)
    return result
