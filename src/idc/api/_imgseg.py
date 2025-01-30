import base64
import io
import logging
from typing import Tuple, Dict, List

import numpy as np
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

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        result = dict()
        if self.annotation.labels is not None:
            result["labels"] = self.annotation.labels[:]
        result["layers"] = dict()
        for label in self.annotation.layers:
            arr = self.annotation.layers[label]
            ann = Image.fromarray(arr, "L").convert("1")
            buffer = io.BytesIO()
            ann.save(buffer, format=self.image_format)
            result["layers"][label] = base64.encodebytes(buffer.getvalue()).decode("ascii")

        return result

    def new_layer(self, label: str) -> np.ndarray:
        """
        Adds an empty layer with the specified label.

        :param label: the label of the layer
        :type label: str
        :return: the generated layer
        :rtype: np.ndarray
        """
        if self.image_size is None:
            raise Exception("No image dimensions available, cannot create empty layer ''%s!" % label)
        if self.annotation is None:
            self.annotation = ImageSegmentationAnnotations(labels=[], layers={})
        width, height = self.image_size
        layer = np.zeros((height, width), dtype=np.uint8)
        if label not in self.annotation.labels:
            self.annotation.labels.append(label)
        self.annotation.layers[label] = layer
        return layer

    def has_layer(self, label: str) -> bool:
        """
        Checks whether the layer is present.

        :param label: the layer to check
        :type label: str
        :return: true if present (may be empty though)
        :rtype: bool
        """
        if not self.has_annotation():
            return False
        return label in self.annotation.layers


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
                    logger: logging.Logger, background: int = 0) -> ImageSegmentationAnnotations:
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
    :param background: the index (0-255) of the background, default 0
    :type background: int
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == background:
            continue
        index = int(index)
        if background < index:
            label_index = index - 1
        else:
            label_index = index
        if label_index not in label_mapping:
            msg = "Index not covered by labels, skipping: %d" % index
            if logger is not None:
                logger.warning(msg)
            else:
                print(msg)
            continue
        sub_arr = np.where(arr == index, 255, 0).astype(np.uint8)
        layers[label_mapping[label_index]] = sub_arr
    return ImageSegmentationAnnotations(labels, layers)


def to_indexedpng(width: int, height: int, ann: ImageSegmentationAnnotations, palette_list: List[int], background: int = 0) -> Image.Image:
    """
    Turns the annotations into an indexed image.

    :param width: the width of the image
    :type width: int
    :param height: the height of the image
    :type height: int
    :param ann: the annotations to convert
    :type ann: ImageSegmentationAnnotations
    :param palette_list: the flat list of int RGB values to use for the palette (len = 3 * #labels)
    :type palette_list: list
    :param background: the background index
    :type background: int
    :return: the generated indexed image
    :rtype: Image.Image
    """
    # combine layers
    arr = np.zeros((height, width)).astype(dtype=np.uint8)
    for index, label in enumerate(ann.labels, start=1):
        if label in ann.layers:
            sub_arr = ann.layers[label]
            sub_arr = np.where(sub_arr == 255, index, 0).astype(np.uint8)
            arr += sub_arr
    if background > 0:
        arr = np.where(arr == 0, background, arr)
    result = Image.fromarray(arr, "P")
    result.putpalette(palette_list)
    return result


def from_bluechannel(img: Image.Image, labels: List[str], label_mapping: Dict[int, str],
                     logger: logging.Logger, background: int = 0) -> ImageSegmentationAnnotations:
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
    :param background: the index (0-255) of the background, default 0
    :type background: int
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    arr = arr[:, :, 2]
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == background:
            continue
        index = int(index)
        if background < index:
            label_index = index - 1
        else:
            label_index = index
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


def to_bluechannel(width: int, height: int, ann: ImageSegmentationAnnotations, background: int = 0) -> Image.Image:
    """
    Turns the annotations into a RGB image with the layers in the blue channel.

    :param width: the width of the image
    :type width: int
    :param height: the height of the image
    :type height: int
    :param ann: the annotations to convert
    :type ann: ImageSegmentationAnnotations
    :param background: the background index
    :type background: int
    :return: the generated RGB image with the layers in the blue channel
    :rtype: Image.Image
    """
    arr = np.zeros((height, width)).astype(dtype=np.uint8)
    for index, label in enumerate(ann.labels, start=1):
        if label in ann.layers:
            sub_arr = ann.layers[label]
            sub_arr = np.where(sub_arr == 255, index, 0).astype(np.uint8)
            arr += sub_arr
    if background > 0:
        arr = np.where(arr == 0, background, arr)
    blue = np.zeros((*arr.shape, 3), np.uint8)
    blue[:, :, 2] = arr
    result = Image.fromarray(blue, "RGB")
    return result


def from_grayscale(img: Image.Image, labels: List[str], label_mapping: Dict[int, str],
                   logger: logging.Logger, background: int = 0) -> ImageSegmentationAnnotations:
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
    :param background: the index (0-255) of the background, default 0
    :type background: int
    :return: the generated annotations
    :rtype: ImageSegmentationAnnotations
    """
    arr = np.asarray(img).astype(np.uint8)
    unique = np.unique(arr)
    layers = dict()
    for index in list(unique):
        # skip background
        if index == background:
            continue
        index = int(index)
        if background < index:
            label_index = index - 1
        else:
            label_index = index
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


def to_grayscale(width: int, height: int, ann: ImageSegmentationAnnotations, background: int = 0) -> Image.Image:
    """
    Turns the annotations into a grayscale image.

    :param width: the width of the image
    :type width: int
    :param height: the height of the image
    :type height: int
    :param ann: the annotations to convert
    :type ann: ImageSegmentationAnnotations
    :param background: the background index
    :type background: int
    :return: the generated grayscale image
    :rtype: Image.Image
    """
    arr = np.zeros((height, width)).astype(dtype=np.uint8)
    for index, label in enumerate(ann.labels, start=1):
        if label in ann.layers:
            sub_arr = ann.layers[label]
            sub_arr = np.where(sub_arr == 255, index, 0).astype(np.uint8)
            arr += sub_arr
    if background > 0:
        arr = np.where(arr == 0, background, arr)
    result = Image.fromarray(arr, "L")
    return result
