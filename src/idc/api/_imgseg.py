import logging
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
        :param layers: the label -> numpy array association, binary (0/255), uint8
        """
        if (labels is not None) and (layers is not None):
            for label in layers:
                if label not in labels:
                    raise Exception("Layer %s is not specified as label!" % label)
        self.labels = labels
        for label in layers:
            if layers[label].dtype != np.uint8:
                raise Exception("Layers must be %s, but got %s for label '%s'!" % (str(np.dtype(np.uint8)), str(layers[label].dtype), label))
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

    def __init__(self, source: str = None, image_name: str = None, data: bytes = None,
                 image: Image.Image = None, image_format: str = None, image_size: Tuple[int, int] = None,
                 metadata: Dict = None, annotation: ImageSegmentationAnnotations = None):

        super().__init__(source=source, image_name=image_name, data=data,
                         image=image, image_format=image_format, image_size=image_size,
                         metadata=metadata, annotation=annotation)

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return (self.annotation is not None) and (len(self.annotation.layers) > 0)


def combine_layers(item: ImageSegmentationData, dtype=np.int32) -> np.ndarray:
    """
    Combines the layers into a single numpy array. The first label gets value 1.

    :param item: the segmentation data to combine
    :type item: ImageSegmentationData
    :param dtype: the data type to use for the array
    :return: the generated array
    :rtype: np.ndarray
    """
    result = np.zeros((item.image_height, item.image_width, 1), dtype=dtype)
    for i, label in enumerate(item.annotation.labels, start=1):
        if label in item.annotation.layers:
            layer = item.annotation.layers[label]
            layer = np.where(layer > 0, i, layer)
            layer = np.expand_dims(layer, axis=-1)
            result += layer
    return result


def split_layers(array: np.ndarray, labels: List[str]) -> ImageSegmentationAnnotations:
    """
    Generates annotations from the annotations array. Assumes the first label having value of 1.

    :param array: the array to turn into annotations
    :type array: np.ndarray
    :param labels: the list of labels to use
    :type labels: list
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    layers = dict()
    unique = set(np.unique(array))
    for i, label in enumerate(labels, start=1):
        if i in unique:
            layer = np.where(array == i, 255, 0)
            layer = np.squeeze(layer)
            layers[label] = layer.astype(np.uint8)
    return ImageSegmentationAnnotations(labels=labels, layers=layers)


def from_indexedpng(img: Image.Image, labels: List[str], label_mapping: Dict[int, str],
                    logger: logging.Logger) -> ImageSegmentationAnnotations:
    """
    Loads the annotations from the indexed png.

    :param img: the image to turn into annotations
    :type img: Image.Image
    :param labels: the list of labels
    :type labels: list
    :param label_mapping: the mapping of index to label
    :type label_mapping: dict
    :param logger: the (optional) logger for logging messages
    :type logger: logging.Logger
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == 0:
            continue
        index = int(index)
        if index not in label_mapping:
            msg = "Index not covered by labels, skipping: %d" % index
            if logger is not None:
                logger.warning(msg)
            else:
                print(msg)
            continue
        sub_arr = np.where(arr == index, 255, 0).astype(np.uint8)
        layers[label_mapping[index]] = sub_arr
    return ImageSegmentationAnnotations(labels, layers)


def from_bluechannel(img: Image.Image, labels: List[str], label_mapping: Dict[int, str],
                     logger: logging.Logger) -> ImageSegmentationAnnotations:
    """
    Loads the annotations from the blue channel.

    :param img: the image to turn into annotations
    :type img: Image.Image
    :param labels: the list of labels
    :type labels: list
    :param label_mapping: the mapping of index to label
    :type label_mapping: dict
    :param logger: the (optional) logger for logging messages
    :type logger: logging.Logger
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    arr = arr[:, :, 2]
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == 0:
            continue
        index = int(index)
        label_index = index - 1
        if label_index not in label_mapping:
            msg = "Blue channel value not covered by labels, skipping: %d" % index
            if logger is not None:
                logger.warning(msg)
            else:
                print(msg)
            continue
        sub_arr = np.where(arr == index, 255, 0).astype(np.uint8)
        layers[label_mapping[label_index]] = sub_arr
    return ImageSegmentationAnnotations(labels, layers)


def from_grayscale(img: Image.Image, labels: List[str], label_mapping: Dict[int, str],
                   logger: logging.Logger) -> ImageSegmentationAnnotations:
    """
    Loads the annotations from the grayscale image.

    :param img: the image to turn into annotations
    :type img: Image.Image
    :param labels: the list of labels
    :type labels: list
    :param label_mapping: the mapping of index to label
    :type label_mapping: dict
    :param logger: the (optional) logger for logging messages
    :type logger: logging.Logger
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == 0:
            continue
        index = int(index)
        label_index = index - 1
        if label_index not in label_mapping:
            msg = "Grayscale value not covered by labels, skipping: %d" % index
            if logger is not None:
                logger.warning(msg)
            else:
                print(msg)
            continue
        sub_arr = np.where(arr == index, 255, 0).astype(np.uint8)
        layers[label_mapping[label_index]] = sub_arr
    return ImageSegmentationAnnotations(labels, layers)
