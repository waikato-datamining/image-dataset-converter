import copy
import logging
from typing import Tuple, Dict, Union, Optional

from PIL import Image
from shapely import Polygon, GeometryCollection, MultiPolygon
from wai.common.adams.imaging.locateobjects import LocatedObject, LocatedObjects
from wai.common.adams.imaging.locateobjects import NormalizedLocatedObjects, NormalizedLocatedObject
from wai.common.adams.imaging.locateobjects import absolute_to_normalized, normalized_to_absolute
from wai.common.geometry import Point as WaiPoint, Polygon as WaiPolygon

from ._data import ImageData
from ._geometry import locatedobject_polygon_to_shapely, locatedobject_bbox_to_shapely

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


def fit_located_object(index: int, region: LocatedObject, annotation: LocatedObject, logger: Optional[logging.Logger]) -> LocatedObject:
    """
    Fits the annotation into the specified region, adjusts size if necessary.

    :param index: the index of the current region, gets added to meta-data if >=0
    :type index: int
    :param region: the region object to fit the annotation in
    :type region: LocatedObject
    :param annotation: the annotation to fit
    :type annotation: LocatedObject
    :param logger: the logger to use, can be None
    :type logger: logging.Logger
    :return: the adjusted annotation
    :rtype: LocatedObject
    """
    sregion = locatedobject_bbox_to_shapely(region)
    sbbox = locatedobject_bbox_to_shapely(annotation)
    sintersect = sbbox.intersection(sregion)
    minx, miny, maxx, maxy = [int(x) for x in sintersect.bounds]
    result = LocatedObject(x=minx-region.x, y=miny-region.y, width=maxx-minx+1, height=maxy-miny+1, **annotation.metadata)
    if index > -1:
        result.metadata["region_index"] = index
        result.metadata["region_xywh"] = "%d,%d,%d,%d" % (region.x, region.y, region.width, region.height)

    if annotation.has_polygon():
        spolygon = locatedobject_polygon_to_shapely(annotation)
    else:
        spolygon = locatedobject_bbox_to_shapely(annotation)

    try:
        sintersect = spolygon.intersection(sregion)
    except:
        msg = "Failed to compute intersection!"
        if logger is None:
            print(msg)
        else:
            logger.warning(msg)
        sintersect = None

    if isinstance(sintersect, GeometryCollection):
        for x in sintersect.geoms:
            if isinstance(x, Polygon):
                sintersect = x
                break
    elif isinstance(sintersect, MultiPolygon):
        for x in sintersect.geoms:
            if isinstance(x, Polygon):
                sintersect = x
                break

    if isinstance(sintersect, Polygon):
        x_list, y_list = sintersect.exterior.coords.xy
        points = []
        for i in range(len(x_list)):
            points.append(WaiPoint(x=x_list[i]-region.x, y=y_list[i]-region.y))
        result.set_polygon(WaiPolygon(*points))
    else:
        msg = "Unhandled geometry type returned from intersection, skipping: %s" % str(type(sintersect))
        if logger is None:
            print(msg)
        else:
            logger.warning(msg)

    return result
