from typing import Tuple, Dict
from PIL import Image
from ._data import ImageData


class ImageSegmentationData(ImageData):
    """
    The annotations are the classification label.
    """

    def __init__(self, source: str = None, name: str = None, data: bytes = None,
                 image: Image = None, image_format: str = None, size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: str = None):

        super().__init__(source=source, name=name, data=data,
                         image=image, image_format=image_format, size=size,
                         metadata=metadata, annotation=annotation)
