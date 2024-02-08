import io
import logging
import os.path
import shutil
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import imagesize
from PIL import Image
from seppl import MetaDataHandler, LoggingHandler


def locate_image(path: str) -> Optional[str]:
    """
    Tries to locate the image (png or jpg) for the given path by replacing its extension.

    :param path: the base path to use
    :type path: str
    :return: the located image, None if not found
    :rtype: str
    """
    noext = os.path.splitext(path)[0]
    images = [
        noext + ".png",
        noext + ".PNG",
        noext + ".jpg",
        noext + ".JPG",
        noext + ".jpeg",
        noext + ".JPEG",
    ]
    for image in images:
        if os.path.exists(image):
            return image
    return None


@dataclass
class ImageData(MetaDataHandler, LoggingHandler):

    _logger: logging.Logger = None
    """ for logging. """

    source: str = None
    """ the full path to the image file. """

    name: str = None
    """ the name of the image file (no path). """

    data: bytes = None
    """ the binary image data. """

    image: Image = None
    """ the Pillow image. """

    format: str = None
    """ the format of the image. """

    size: Tuple[int, int] = None
    """ the size (width, height) tuple of the image. """

    metadata: Dict = None
    """ the dictionary with optional meta-data. """

    annotation = None
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

    def pillow_image(self) -> Image:
        """
        Returns the image, loads it if necessary.

        :return: the pillow image data structure
        :rtype: Image
        """
        if self.image is not None:
            return self.image
        if self.data is not None:
            self.image = Image.open(io.BytesIO(self.data))
            self.format = self.image.format
            return self.pillow_image()
        if self.source is not None:
            self.name = os.path.basename(self.source)
            self.image = Image.open(self.source)
            self.format = self.image.format
            return self.pillow_image()
        return None

    def image_name(self) -> Optional[str]:
        """
        Returns the name of the image.

        :return: the image name, can be None
        :rtype: str
        """
        if self.name is not None:
            return self.name
        elif self.source is not None:
            return os.path.basename(self.source)
        else:
            return None

    def image_size(self) -> Optional[Tuple[int, int]]:
        """
        Returns the size tuple (width, height) for the image.

        :return: the width/height tuple, None if failed to determine
        :rtype: tuple
        """
        if self.size is not None:
            return self.size
        elif self.data is not None:
            self.size = imagesize.get(self.data)
            return self.size
        elif self.source is not None:
            self.size = imagesize.get(self.source)
            return self.size
        return None

    def save_image(self, path: str) -> bool:
        """
        Saves the image under the specified path.

        :param path: the path to save the image under
        :type path: str
        :return: whether the file was saved
        :rtype: bool
        """
        if (self.data is None) and (self.source is not None) and (os.path.exists(self.source)):
            shutil.copy(self.source, path)
            return True
        if self.image is not None:
            self.image.save(path)
            return True
        if self.data is not None:
            with open(path, "wb") as fp:
                fp.write(self.data)
            return True
        return False

    def has_metadata(self) -> bool:
        """
        Returns whether meta-data is present.

        :return: True if meta-data present
        :rtype: bool
        """
        return self.metadata is not None

    def get_metadata(self) -> Optional[Dict]:
        """
        Returns the meta-data.

        :return: the meta-data, None if not available
        :rtype: dict
        """
        return self.metadata

    def set_metadata(self, metadata: Optional[Dict]):
        """
        Sets the meta-data to use.

        :param metadata: the new meta-data, can be None
        :type metadata: dict
        """
        self.metadata = metadata
