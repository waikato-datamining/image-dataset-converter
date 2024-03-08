import logging
import os.path
import shutil
from typing import Dict, Optional, Tuple

import imagesize
from PIL import Image
from seppl import MetaDataHandler, LoggingHandler
from ._utils import load_image_from_bytes


class ImageData(MetaDataHandler, LoggingHandler):

    def __init__(self, source: str = None, name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation=None):
        self._logger = None
        """ for logging. """
        self._source = source
        """ the full path to the image file. """
        self._name = name
        """ the name of the image file (no path). """
        self._data = data
        """ the binary image data. """
        self._image = image
        """ the Pillow image. """
        self._format = image_format
        """ the format of the image. """
        self._size = size
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
            self._format = self._image.format
            return self._image
        if self._source is not None:
            self._name = os.path.basename(self._source)
            self._image = Image.open(self._source)
            self._format = self._image.format
            return self._image
        return None

    @property
    def image_name(self) -> Optional[str]:
        """
        Returns the name of the image.

        :return: the image name, can be None
        :rtype: str
        """
        if self._name is not None:
            return self._name
        elif self.source is not None:
            return os.path.basename(self.source)
        else:
            return None

    @property
    def image_format(self) -> Optional[str]:
        """
        Returns the format of the image.

        :return: the image format, can be None
        :rtype: str
        """
        if self._format is None:
            if self.image is None:
                return None
        return self._format

    @property
    def image_size(self) -> Optional[Tuple[int, int]]:
        """
        Returns the size tuple (width, height) for the image.

        :return: the width/height tuple, None if failed to determine
        :rtype: tuple
        """
        if self._size is not None:
            return self._size
        elif self._data is not None:
            self._size = imagesize.get(self._data)
            return self._size
        elif self._source is not None:
            self._size = imagesize.get(self._source)
            return self._size
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
        if make_dirs:
            parent_dir = os.path.dirname(path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        if (self._data is None) and (self._source is not None) and (os.path.exists(self._source)):
            shutil.copy(self._source, path)
            return True
        if self._image is not None:
            self._image.save(path)
            return True
        if self._data is not None:
            with open(path, "wb") as fp:
                fp.write(self._data)
            return True
        return False

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
