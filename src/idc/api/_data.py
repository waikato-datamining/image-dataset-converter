import base64
import copy
import io
import logging
import os.path
import shutil
from typing import Dict, Optional, Tuple, List, Union

import imagesize
import numpy as np
from PIL import Image
from image_complete.bmp import is_bmp
from image_complete.jpg import is_jpg
from image_complete.png import is_png
from seppl import MetaDataHandler, LoggingHandler
from ._utils import load_image_from_bytes, safe_deepcopy
from wai.logging import set_logging_level, LOGGING_INFO

_logger = None

FORMAT_JPEG = "JPEG"
FORMAT_PNG = "PNG"
FORMAT_BMP = "BMP"
FORMATS = [
    FORMAT_JPEG,
    FORMAT_PNG,
    FORMAT_BMP,
]
FORMAT_EXTENSIONS = {
    FORMAT_JPEG: ".jpg",
    FORMAT_PNG: ".png",
    FORMAT_BMP: ".bmp",
}

IDC_JPEG_QUALITY = "IDC_JPEG_QUALITY"
""" the environment variable to overriding the default JPEG quality. """

DEFAULT_JPEG_QUALITY = 90
""" the default quality to use when saving jpg/jpeg files. """

JPEG_QUALITY = None
""" the quality to use when writing JPEG files. """


def logger() -> logging.Logger:
    """
    Returns the logger instance to use, initializes it if necessary.

    :return: the logger instance
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("idc.api.data")
        set_logging_level(_logger, LOGGING_INFO)
    return _logger


def jpeg_quality() -> int:
    """
    Returns the quality to use for jpeg images.

    :return: the quality
    :rtype: int
    """
    global JPEG_QUALITY
    if JPEG_QUALITY is None:
        try:
            JPEG_QUALITY = DEFAULT_JPEG_QUALITY
            if IDC_JPEG_QUALITY in os.environ:
                JPEG_QUALITY = int(os.getenv(IDC_JPEG_QUALITY, str(DEFAULT_JPEG_QUALITY)))
                logger().info("Using JPEG quality: %d%%" % JPEG_QUALITY)
        except:
            JPEG_QUALITY = DEFAULT_JPEG_QUALITY
    return JPEG_QUALITY


def save_image(img: Image.Image, path: str, make_dirs: bool = False):
    """
    Saves the image in the specified location.
    For JPEG images, takes the quality into account.

    :param img: the image to save
    :type img: Image.Image
    :param path: the path to save the image to
    :type path: str
    :param make_dirs: whether to create parent dirs if necessary
    :type make_dirs: bool
    """
    if make_dirs:
        parent_dir = os.path.dirname(path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
    if img.format == "JPEG":
        img.save(path, quality=jpeg_quality())
    else:
        img.save(path)


def array_to_image(array: Union[np.ndarray, Image.Image], image_format: str) -> Tuple[Image.Image, io.BytesIO]:
    """
    Turns the numpy array back into an image of the specified format.
    Returns the image data structure and the bytes representing it.
    For JPEG images, takes the quality into account.

    :param array: the Image/array to convert
    :type array: np.ndarray or Image.Image
    :param image_format: the image format to generate
    :type image_format: str
    :return: the generated image data structure
    :rtype: tuple
    """
    img = Image.fromarray(np.uint8(array))
    img_bytes = io.BytesIO()
    if image_format == "JPEG":
        img.save(img_bytes, format=image_format, quality=jpeg_quality())
    else:
        img.save(img_bytes, format=image_format)
    return img, img_bytes


def empty_image(mode: str, width: int, height: int, image_format: str) -> Tuple[Image.Image, io.BytesIO]:
    """
    Creates an empty image and returns the image and the bytes representation.

    :param mode: the image mode, e.g., RGB
    :type mode: str
    :param width: the width of the image
    :type width: int
    :param height: the height of the image
    :type height: int
    :param image_format: the image format to use, e.g., JPEG
    :type image_format: str
    :return: the tuple of image and bytes
    :rtype: tuple
    """
    img = Image.new(mode, (width, height))
    img_bytes = io.BytesIO()
    if image_format == "JPEG":
        img.save(img_bytes, format=image_format, quality=jpeg_quality())
    else:
        img.save(img_bytes, format=image_format)
    return img, img_bytes


class ImageData(MetaDataHandler, LoggingHandler):

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation=None):
        self._logger = None
        """ for logging. """
        self._source = source
        """ the full path to the image file. """
        self._image_name = image_name
        """ the name of the image file (no path). """
        self._data = data
        """ the binary image data. """
        self._image = image
        """ the Pillow image. """
        self._image_format = image_format
        """ the format of the image. """
        self._image_size = image_size
        """ the size (width, height) tuple of the image. """
        self._metadata = metadata
        """ the dictionary with optional meta-data. """
        self.annotation = annotation
        """ the associated annotation data. """

    def logger(self) -> logging.Logger:
        """
        Returns the logger instance to use.

        :return: the logger
        :rtype: logging.Logger
        """
        if self._logger is None:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    @property
    def source(self) -> Optional[str]:
        """
        Returns the source filename.

        :return: the full filename, if available
        :rtype: str
        """
        return self._source

    @property
    def image(self) -> Image.Image:
        """
        Returns the image, loads it if necessary.

        :return: the pillow image data structure, None if not available or failed to load
        :rtype: Image.Image
        """
        if self._image is not None:
            return self._image
        if self._data is not None:
            self._image = load_image_from_bytes(self._data)
            self._image_format = self._image.format
            return self._image
        if self._source is not None:
            self._image_name = os.path.basename(self._source)
            self._image = Image.open(self._source)
            self._image_format = self._image.format
            return self._image
        return None

    @property
    def image_bytes(self):
        """
        Turns the pillow image into bytes using the current image format.

        :return: the generated bytes
        """
        buffer = io.BytesIO()
        if self.image is not None:
            self.image.save(buffer, format=self.image_format)
        return buffer.getvalue()

    @property
    def image_name(self) -> Optional[str]:
        """
        Returns the name of the image.

        :return: the image name, can be None
        :rtype: str
        """
        if self._image_name is not None:
            return self._image_name
        elif self.source is not None:
            return os.path.basename(self.source)
        else:
            return None

    @image_name.setter
    def image_name(self, s: str):
        """
        Sets the new name.

        :param s: the new name
        :type s: str
        """
        self._image_name = s

    @property
    def image_format(self) -> Optional[str]:
        """
        Returns the format of the image.

        :return: the image format, can be None
        :rtype: str
        """
        if self._image_format is None:
            if self.source is not None:
                to_check = self.source
            else:
                to_check = self.data
            if to_check is not None:
                if is_jpg(to_check):
                    self._image_format = FORMAT_JPEG
                elif is_png(to_check):
                    self._image_format = FORMAT_PNG
                elif is_bmp(to_check):
                    self._image_format = FORMAT_BMP
        if self._image_format is None:
            if self.image is None:
                return None
        return self._image_format

    @property
    def image_size(self) -> Optional[Tuple[int, int]]:
        """
        Returns the size tuple (width, height) for the image.

        :return: the width/height tuple, None if failed to determine
        :rtype: tuple
        """
        if self._image_size is not None:
            return self._image_size

        if self._data is not None:
            try:
                self._image_size = imagesize.get(self._data)
                return self._image_size
            except:
                pass

        if self._source is not None:
            try:
                self._image_size = imagesize.get(self._source)
                return self._image_size
            except:
                pass

        if self.image is not None:
            return self.image.size

        return None

    @property
    def image_width(self) -> Optional[int]:
        """
        Returns the width of the image.

        :return: the width, None if failed to determine
        :rtype: int
        """
        size = self.image_size
        if size is None:
            return None
        else:
            return size[0]

    @property
    def image_height(self) -> Optional[int]:
        """
        Returns the height of the image.

        :return: the height, None if failed to determine
        :rtype: int
        """
        size = self.image_size
        if size is None:
            return None
        else:
            return size[1]

    @property
    def data(self) -> bytes:
        """
        Returns the internal data, if any.

        :return: the data
        """
        return self._data

    @data.setter
    def data(self, data: bytes):
        """
        Uses the provided data.

        :param data: the data to use
        """
        self._image_name = self.image_name
        self._source = None
        self._image_format = None
        self._image_size = None
        self._data = data

    def save_image(self, path: str, make_dirs: bool = False) -> bool:
        """
        Saves the image under the specified path.

        :param path: the path to save the image under
        :type path: str
        :param make_dirs: whether to create any missing parent dirs
        :type make_dirs: bool
        :return: whether the file was saved
        :rtype: bool
        """
        if self._source is not None:
            if os.path.exists(path) and os.path.exists(self._source) and os.path.samefile(path, self._source):
                self.logger().warning("Input/output image are the same, skipping!")
                return False
        if make_dirs:
            parent_dir = os.path.dirname(path)
            if not os.path.exists(parent_dir):
                self.logger().info("Creating dir: %s" % parent_dir)
                os.makedirs(parent_dir)
        if (self._data is None) and (self._source is not None) and (os.path.exists(self._source)):
            shutil.copy(self._source, path)
            return True
        if self._image is not None:
            save_image(self._image, path)
            return True
        if self._data is not None:
            with open(path, "wb") as fp:
                fp.write(self._data)
            return True
        return False

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return self.annotation is not None

    def has_metadata(self) -> bool:
        """
        Returns whether meta-data is present.

        :return: True if meta-data present
        :rtype: bool
        """
        return self._metadata is not None

    def get_metadata(self) -> Optional[Dict]:
        """
        Returns the meta-data.

        :return: the meta-data, None if not available
        :rtype: dict
        """
        return self._metadata

    def set_metadata(self, metadata: Optional[Dict]):
        """
        Sets the meta-data to use.

        :param metadata: the new meta-data, can be None
        :type metadata: dict
        """
        self._metadata = metadata

    def duplicate(self, source: str = None, force_no_source: bool = None,
                  name: str = None, data: bytes = None,
                  image: Image.Image = None, image_format: str = None,
                  size: Tuple[int, int] = None,
                  metadata: Dict = None, annotation=None):
        """
        Duplicates the container overwriting existing data with any provided data.

        :param source: the source to use
        :type source: str
        :param force_no_source: if True, then source is set to None
        :type force_no_source: bool
        :param name: the name to use
        :type name: str
        :param data: the data to use
        :type data: bytes
        :param image: the Pillow image to use
        :type image: Image.Image
        :param image_format: the image format
        :type image_format: str
        :param size: the size tuple
        :type size: tuple
        :param metadata: the metadata
        :type metadata: dict
        :param annotation: the annotations
        :return: the duplicated container
        """
        if (force_no_source is not None) and force_no_source:
            source = None
        else:
            if source is None:
                source = self._source
        if name is None:
            name = self._image_name
        if data is None:
            data = safe_deepcopy(self._data)
        # if the source changes, we need to force loading the image
        if ((image is None) and (self._image is not None)) or (source != self._source):
            image = copy.deepcopy(self.image)
        if image_format is None:
            image_format = self._image_format
        if size is None:
            size = safe_deepcopy(self._image_size)
        if metadata is None:
            metadata = safe_deepcopy(self._metadata)
        if annotation is None:
            annotation = safe_deepcopy(self.annotation)

        return type(self)(source=source, image_name=name, data=data,
                          image=image, image_format=image_format, image_size=size,
                          metadata=metadata, annotation=annotation)

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        raise NotImplementedError()

    def to_dict(self, source: bool = True, image: bool = True, annotation: bool = True, metadata: bool = True):
        """
        Returns itself as a dictionary that can be saved as JSON.

        :param source: whether to include the source
        :type source: bool
        :param image: whether to include the image
        :type image: bool
        :param annotation: whether to include the annotations
        :type annotation: bool
        :param metadata: whether to include the metadata
        :type metadata: bool
        :return: the generated dictionary
        :rtype: dict
        """
        result = dict()
        if source and (self.source is not None):
            result["source"] = self.source
        if self.image_name is not None:
            result["name"] = self.image_name
        if self.image_format is not None:
            result["format"] = self.image_format
        if self.image_width is not None:
            result["width"] = self.image_width
        if self.image_height is not None:
            result["height"] = self.image_height
        if image:
            result["image"] = base64.encodebytes(self.image_bytes).decode("ascii")
        if annotation and (self.annotation is not None):
            result["annotation"] = self._annotation_to_dict()
        if metadata and (self.get_metadata() is not None):
            result["metadata"] = copy.deepcopy(self.get_metadata())
        return result


def make_list(data, cls=ImageData) -> List:
    """
    Wraps the data item in a list if not already a list.

    :param data: the data item to wrap if necessary
    :param cls: the type of class to check for
    :return: the list
    :rtype: list
    """
    if isinstance(data, cls):
        data = [data]
    return data


def flatten_list(data: List):
    """
    If the list contains only a single item, then it returns that instead of a list.

    :param data: the list to check
    :type data: list
    :return: the list or single item
    """
    if len(data) == 1:
        return data[0]
    else:
        return data
