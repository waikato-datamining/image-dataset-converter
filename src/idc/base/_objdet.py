from dataclasses import dataclass
from typing import Union

from ._data import ImageData
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.common.adams.imaging.locateobjects import absolute_to_normalized, normalized_to_absolute


@dataclass
class ObjectDetectionData(ImageData):

    annotation: Union[LocatedObjects, NormalizedLocatedObjects] = None
    """ the annotations. """

    def is_normalized(self) -> bool:
        """
        Returns whether the annotations are normalized or absolute.

        :return: True if normalized
        :rtype: bool
        """
        return isinstance(self.annotation, NormalizedLocatedObjects)

    def get_normalized(self) -> NormalizedLocatedObjects:
        """
        Returns normalized annotations.
        """
        if self.is_normalized():
            return self.annotation
        else:
            width, height = self.image_size()
            return absolute_to_normalized(self.annotation, width, height)

    def to_normalized(self):
        """
        Turns the absolute annotations into normalized ones (in-place).
        """
        if self.is_normalized():
            return
        self.annotation = self.get_normalized()

    def get_absolute(self) -> LocatedObjects:
        """
        Returns absolute annotations.
        """
        if not self.is_normalized():
            return self.annotation
        else:
            width, height = self.image_size()
            return normalized_to_absolute(self.annotation, width, height)

    def to_absolute(self):
        """
        Turns the normalized annotations into absolute ones (in-place).
        """
        if not self.is_normalized():
            return
        self.annotation = self.get_absolute()
