from PIL import Image
from typing import Tuple, Dict, Union, Optional

from ._data import ImageData
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.common.adams.imaging.locateobjects import absolute_to_normalized, normalized_to_absolute


class ObjectDetectionData(ImageData):
    """
    The annotations are LocatedObjects or NormalizedLocatedObjects.
    """

    def __init__(self, source: str = None, name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: Union[LocatedObjects, NormalizedLocatedObjects] = None):

        super().__init__(source=source, name=name, data=data,
                         image=image, image_format=image_format, size=size,
                         metadata=metadata, annotation=annotation)

    def is_normalized(self) -> bool:
        """
        Returns whether the annotations are normalized or absolute.

        :return: True if normalized
        :rtype: bool
        """
        return isinstance(self.annotation, NormalizedLocatedObjects)

    def get_normalized(self) -> Optional[NormalizedLocatedObjects]:
        """
        Returns normalized annotations.
        """
        if self.annotation is None:
            return None
        if isinstance(self.annotation, NormalizedLocatedObjects):
            return self.annotation
        if self.image_size is None:
            return None
        if isinstance(self.annotation, LocatedObjects):
            width, height = self.image_size
            return absolute_to_normalized(self.annotation, width, height)
        raise Exception("Unhandled type of annotations: %s" % str(type(self.annotation)))

    def to_normalized(self):
        """
        Turns the absolute annotations into normalized ones (in-place).
        """
        if self.is_normalized():
            return
        self.annotation = self.get_normalized()

    def get_absolute(self) -> Optional[LocatedObjects]:
        """
        Returns absolute annotations.

        :return: the absolute annotations, None if not available
        :rtype: LocatedObjects
        """
        if self.annotation is None:
            return None
        if isinstance(self.annotation, LocatedObjects):
            return self.annotation
        if self.image_size is None:
            return None
        if isinstance(self.annotation, NormalizedLocatedObjects):
            width, height = self.image_size
            return normalized_to_absolute(self.annotation, width, height)
        raise Exception("Unhandled type of annotations: %s" % str(type(self.annotation)))

    def to_absolute(self):
        """
        Turns the normalized annotations into absolute ones (in-place).
        """
        if not self.is_normalized():
            return
        self.annotation = self.get_absolute()
