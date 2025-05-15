import base64
import numpy as np
from PIL import Image
from typing import Tuple, Dict

from ._data import ImageData


ACCEPTED_DEPTH_TYPES = [np.uint8, np.float32]


class DepthInformation:
    """
    Container for depth information.
    """

    def __init__(self, data: np.ndarray = None):
        """
        Initializes the depth information.

        :param data: the depth data to use (2-dim array either float32 or uint8), can be None
        """
        if data is not None:
            if len(data.shape) != 2:
                raise Exception("Depth information data must have two dimension, but got instead: %s" % str(data.shape))
            if data.dtype not in ACCEPTED_DEPTH_TYPES:
                raise Exception("Unsupported depth information type: %s (accepted: %s)" % (str(data.dtype), str(ACCEPTED_DEPTH_TYPES)))
        self.data = data

    @property
    def size(self):
        """
        Returns the size of the underlying depth matrix.

        :return: the size
        :rtype: int
        """
        return self.data.size


class DepthData(ImageData):
    """
    The annotations are the depth information matrix.
    """

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: DepthInformation = None):

        super().__init__(source=source, image_name=image_name, data=data,
                         image=image, image_format=image_format, image_size=image_size,
                         metadata=metadata, annotation=annotation)

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return (self.annotation is not None) and (self.annotation.size > 0)

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {
            "depth": base64.encodebytes(self.annotation.data.tobytes()).decode("ascii")
        }
