from dataclasses import dataclass

from ._data import ImageData
from wai.common.adams.imaging.locateobjects import LocatedObjects


@dataclass
class ObjectDetectionData(ImageData):

    annotation: LocatedObjects = None
    """ the annotations. """
