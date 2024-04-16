from PIL import Image
from typing import Tuple, Dict

from ._data import ImageData


class ImageClassificationData(ImageData):
    """
    The annotations are the classification label.
    """

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: str = None):

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

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {"label": self.annotation}
