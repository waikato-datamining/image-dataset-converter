from dataclasses import dataclass
from typing import Union

from ._data import ImageData
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects


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
