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

    def to_normalized(self):
        """
        Turns the absolute annotations into normalized ones (in-place).
        """
        if self.is_normalized():
            return
        width, height = self.image_size()
        self.annotation = absolute_to_normalized(self.annotation, width, height)

    def to_absolute(self):
        """
        Turns the normalized annotations into absolute ones (in-place).
        """
        if not self.is_normalized():
            return
        width, height = self.image_size()
        self.annotation = normalized_to_absolute(self.annotation, width, height)
