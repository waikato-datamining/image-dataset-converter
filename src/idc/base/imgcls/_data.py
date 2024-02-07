from dataclasses import dataclass

from .._data import ImageData


@dataclass
class ImageClassificationData(ImageData):

    annotation: str = None
    """ the classification label. """
