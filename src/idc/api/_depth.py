import base64
import logging
import numpy as np
from PIL import Image
from typing import Tuple, Dict

from ._data import ImageData


ACCEPTED_DEPTH_TYPES = [np.uint8, np.float32]


class DepthInformation:
    """
    Container for depth information.
    """

    def __init__(self, data: np.ndarray = None):
        """
        Initializes the depth information.

        :param data: the depth data to use (2-dim array either float32 or uint8), can be None
        """
        if data is not None:
            if len(data.shape) != 2:
                raise Exception("Depth information data must have two dimension, but got instead: %s" % str(data.shape))
            if data.dtype not in ACCEPTED_DEPTH_TYPES:
                raise Exception("Unsupported depth information type: %s (accepted: %s)" % (str(data.dtype), str(ACCEPTED_DEPTH_TYPES)))
        self.data = data

    @property
    def size(self):
        """
        Returns the size of the underlying depth matrix.

        :return: the size
        :rtype: int
        """
        return self.data.size


class DepthData(ImageData):
    """
    The annotations are the depth information matrix.
    """

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: DepthInformation = None):

        super().__init__(source=source, image_name=image_name, data=data,
                         image=image, image_format=image_format, image_size=image_size,
                         metadata=metadata, annotation=annotation)

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return (self.annotation is not None) and (self.annotation.size > 0)

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {
            "depth": base64.encodebytes(self.annotation.data.tobytes()).decode("ascii")
        }


def depth_to_grayscale(ann: DepthInformation, min_value: float = None, max_value: float = None,
                       logger: logging.Logger = None) -> Image.Image:
    """
    Turns the depth information into a grayscale image.

    :param ann: the depth information
    :type ann: DepthInformation
    :param min_value: whether to use a lower limit for the depth, ignored if None
    :type min_value: float
    :param max_value: whether to use an upper limit for the depth, ignored if None
    :type max_value: float
    :param logger: optional logger instance for outputting some info
    :type logger: logging.Logger
    :return: the grayscale image generated from the depth info
    :rtype: Image.Image
    """
    array = ann.data

    # apply min/max
    if min_value is not None:
        if logger is not None:
            logger.info("applying min value: %s" % str(min_value))
        array = np.where(array < min_value, min_value, array)
    if max_value is not None:
        if logger is not None:
            logger.info("applying max value: %s" % str(max_value))
        array = np.where(array > max_value, max_value, array)

    # scale to 0-255
    min_val = np.min(array)
    if logger is not None:
        logger.info("min: %s" % str(min_val))
    max_val = np.max(array)
    if logger is not None:
        logger.info("max: %s" % str(max_val))
    array -= min_val
    if max_val != 0:
        array *= 255.0 / max_val
    array = array.astype(np.uint8)

    # grayscale image
    result = Image.fromarray(array, 'L')
    return result


def depth_from_grayscale(img: Image.Image, min_value: float = None, max_value: float = None,
                         logger: logging.Logger = None) -> DepthInformation:
    """
    Loads the depth information from the grayscale image.

    :param img: the grayscale image with the depth information
    :type img: Image.Image
    :param min_value: whether to use a lower limit for the depth, ignored if None
    :type min_value: float
    :param max_value: whether to use an upper limit for the depth, ignored if None
    :type max_value: float
    :param logger: optional logger instance for outputting some info
    :type logger: logging.Logger
    :return: the depth information generated from the image
    :rtype: DepthInformation
    """
    arr = np.asarray(img).astype(np.float32)
    if (min_value is not None) and (max_value is not None):
        arr /= 255 * (max_value - min_value)
        arr += min_value
        if logger is not None:
            logger.info("New min=%s and max=%s" % (str(np.min(arr)), str(np.max(arr))))
    elif min_value is not None:
        arr += min_value
        if logger is not None:
            logger.info("New min=%s" % str(np.min(arr)))
    return DepthInformation(arr)
