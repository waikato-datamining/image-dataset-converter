import copy
from typing import Tuple, Dict, Union, Optional

from PIL import Image
from wai.common.adams.imaging.locateobjects import LocatedObject, LocatedObjects
from wai.common.adams.imaging.locateobjects import NormalizedLocatedObjects, NormalizedLocatedObject
from wai.common.adams.imaging.locateobjects import absolute_to_normalized, normalized_to_absolute

from ._data import ImageData

DEFAULT_LABEL = "object"

LABEL_KEY = "type"


def get_object_label(located_object: Union[LocatedObject, NormalizedLocatedObject], default_label: Optional[str] = DEFAULT_LABEL) -> Optional[str]:
    """
    Returns the object label from the located object.

    :param located_object: the located object to get the label from the meta-data
    :type located_object: LocatedObject
    :param default_label: the default label to use in case no label is stored in meta-data
    :type default_label: str
    :return: the label
    :rtype: str
    """
    if LABEL_KEY in located_object.metadata:
        return str(located_object.metadata[LABEL_KEY])
    else:
        return default_label


def set_object_label(located_object: Union[LocatedObject, NormalizedLocatedObject], label: str):
    """
    Sets the object label for the located object.

    :param located_object: the located object to set the label for in its meta-data
    :type located_object: LocatedObject
    :param label: the label to set
    :type label: str
    """
    located_object.metadata[LABEL_KEY] = label


class ObjectDetectionData(ImageData):
    """
    The annotations are LocatedObjects or NormalizedLocatedObjects.
    """

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: Union[LocatedObjects, NormalizedLocatedObjects] = None):

        super().__init__(source=source, image_name=image_name, data=data,
                         image=image, image_format=image_format, image_size=image_size,
                         metadata=metadata, annotation=annotation)

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return (self.annotation is not None) and (len(self.annotation) > 0)

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

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        objs = []
        for lobj in self.annotation:
            obj = dict()
            obj["x"] = lobj.x
            obj["y"] = lobj.y
            obj["width"] = lobj.width
            obj["height"] = lobj.height
            obj["metadata"] = copy.deepcopy(lobj.metadata)
            if lobj.has_polygon():
                obj["poly_x"] = lobj.get_polygon_x()
                obj["poly_y"] = lobj.get_polygon_y()
            objs.append(obj)

        result = dict()
        result["objects"] = objs
        result["normalized"] = self.is_normalized()

        return result
