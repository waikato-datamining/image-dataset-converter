import numpy as np
from typing import Tuple, Dict, List
from PIL import Image
from ._data import ImageData


class ImageSegmentationAnnotations:
    """
    Container for image segmentation annotations.
    """

    def __init__(self, labels: List[str] = None, layers: Dict[str, np.ndarray] = None):
        """
        Initializes the container.

        :param labels: the list of labels
        :param layers: the label -> pillow image assocation
        """
        if (labels is not None) and (layers is not None):
            for label in layers:
                if label not in labels:
                    raise Exception("Layer %s is not specified as label!" % label)
        self.labels = labels
        self.layers = layers

    def subset(self, labels: List[str]) -> 'ImageSegmentationAnnotations':
        """
        Returns the subset of annotations based on the supplied labels.

        :param labels: the labels that will make up the subset
        :type labels: list
        :return: the new annotations
        :rtype: ImageSegmentationData
        """
        layers = dict()
        for label in labels:
            if label in self.layers:
                layers[label] = self.layers[label]
        return ImageSegmentationAnnotations(labels=labels, layers=layers)


class ImageSegmentationData(ImageData):
    """
    The annotations are the classification label.
    """

    def __init__(self, source: str = None, name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: ImageSegmentationAnnotations = None):

        super().__init__(source=source, name=name, data=data,
                         image=image, image_format=image_format, size=size,
                         metadata=metadata, annotation=annotation)
