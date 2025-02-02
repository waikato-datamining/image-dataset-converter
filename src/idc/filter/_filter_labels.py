import argparse
import copy
import numpy as np
import re
from shapely.geometry import Polygon
from typing import List, Dict

from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject, normalized_to_absolute, \
    NormalizedLocatedObjects
from seppl.io import Filter
from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, locatedobject_polygon_to_shapely, \
    intersect_over_union, get_object_label, flatten_list, make_list


class FilterLabels(Filter):
    """
    Filters out labels according to the parameters.
    """

    def __init__(self, labels: List[str] = None, regexp: str = None,
                 region: str = None, min_iou: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param labels: the labels to use
        :type labels: list
        :param regexp: the regular expression for using only a subset
        :type regexp: str
        :param region: region that the object must overlap with in order to be included (object detection only). Between 0-1 the values are considered normalized, otherwise absolute pixels. format: x,y,w,h
        :type region: str
        :param min_iou: the minimum IoU (intersect over union) that the object must have with the region in order to be considered an overlap (object detection only)
        :type min_iou: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.labels = labels
        self.regexp = regexp
        self.region = region
        self.min_iou = min_iou
        self._pattern = None
        self._region = None
        self._normalized = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "filter-labels"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Filters out labels according to the parameters."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData, ImageClassificationData, ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData, ImageClassificationData, ImageSegmentationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--labels", type=str, default=None, help="The labels to use", required=False, nargs="*")
        parser.add_argument("--regexp", type=str, default=None, help="Regular expression for using only a subset of labels", required=False)
        parser.add_argument("--region", type=str, default=None, metavar="x,y,w,h", help="Region that the object must overlap with in order to be included (object detection only). Between 0-1 the values are considered normalized, otherwise absolute pixels.", required=False)
        parser.add_argument("--min_iou", type=float, default=None, help="The minimum IoU (intersect over union) that the object must have with the region in order to be considered an overlap (object detection only)", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.labels = ns.labels
        self.regexp = ns.regexp
        self.region = ns.region
        self.min_iou = ns.min_iou

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if self.labels is None:
            self.labels = []

        self._pattern = re.compile(self.regexp) if (self.regexp is not None) else None

        if self.region is None:
            self._region = None
            self._normalized = False
        else:
            parts = self.region.split(",")
            if len(parts) != 4:
                raise Exception("Region must have format 'x,y,w,h', but found: %s" % self.region)
            self._region = [float(x) for x in parts]
            self._normalized = sum([(0 if (x < 1) else 1) for x in self._region]) < 4

    def remove_invalid_objects(self, located_objects: LocatedObjects, width: int, height: int) -> LocatedObjects:
        """
        Removes objects with labels that are not valid under the given options.

        :param located_objects: The located objects to process.
        :param width: the width of the image
        :type width: int
        :param height: the height of the image
        :type height: int
        :return: the (potentially) updated objects
        :rtype: LocatedObjects
        """
        # Create a list of objects to remove
        invalid_objects: List[int] = []

        if isinstance(located_objects, NormalizedLocatedObjects):
            absolute = normalized_to_absolute(located_objects, width, height)
        else:
            absolute = located_objects

        # Search the located objects
        for index, located_object in enumerate(absolute):
            if not self.filter_object(located_object):
                invalid_objects.append(index)
            elif not self.filter_region(located_object, width, height):
                invalid_objects.append(index)

        # Remove the invalid objects
        if len(invalid_objects) > 0:
            located_objects = copy.deepcopy(located_objects)
            for index in reversed(invalid_objects):
                located_objects.pop(index)

        return located_objects

    def filter_label(self, label: str) -> bool:
        """
        Filter function which selects labels that match the given options.

        :param label:   The label to test.
        :return:        True if the label matches, false if not.
        """
        if len(self.labels) == 0 and self._pattern is None:
            return True
        elif len(self.labels) == 0:
            return bool(self._pattern.match(label))
        elif self._pattern is None:
            return label in self.labels
        else:
            return bool(self._pattern.match(label)) or label in self.labels

    def filter_object(self, located_object: LocatedObject) -> bool:
        """
        Filter function which selects objects whose labels match the given options.

        :param located_object:  The located object to test.
        :return:                True if the object matches, false if not.
        """
        # Filter the label
        label = get_object_label(located_object)
        return self.filter_label(label)

    def filter_region(self, located_object: LocatedObject, width: int, height: int) -> bool:
        """
        Ensures that the object fits into the defined region.

        :param located_object: the object to check
        :param width: the width of the image
        :type width: int
        :param height: the height of the image
        :type height: int
        :return: True if the objects overlaps the region or no region defined at all
        """
        if self._region is None:
            return True

        if self._normalized:
            x = int(self._region[0] * width)
            y = int(self._region[1] * height)
            w = int(self._region[2] * width)
            h = int(self._region[3] * height)
        else:
            x = self._region[0]
            y = self._region[1]
            w = self._region[2]
            h = self._region[3]

        object_poly = locatedobject_polygon_to_shapely(located_object)
        region_poly = Polygon([(x, y), (x+w-1, y), (x+w-1, y+h-1), (x, y+h-1)])
        iou = intersect_over_union(object_poly, region_poly)

        return iou > self.min_iou

    def remove_invalid_layers(self, layers: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Removes all invalid layers.

        :param layers: the layers to process
        :type layers: dict
        :return: the updated layers
        :rtype: dict
        """
        delete = []
        for label in layers:
            if not self.filter_label(label):
                delete.append(label)
        if len(delete) > 0:
            layers = copy.deepcopy(layers)
            for label in delete:
                del layers[label]
        return layers

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if isinstance(item, ObjectDetectionData):
                # Use the options to filter the located objects by label
                objects_new = self.remove_invalid_objects(item.annotation, item.image_width, item.image_height)
                # no annotations left? mark as negative
                if len(objects_new) == 0:
                    item_new = item.duplicate()
                    item_new.annotation = None
                    result.append(item_new)
                else:
                    item_new = item.duplicate()
                    item_new.annotation = objects_new
                    result.append(item_new)
            elif isinstance(item, ImageClassificationData):
                # mark as negative if label doesn't match
                if not self.filter_label(item.annotation):
                    item_new = item.duplicate()
                    item_new.annotation = None
                    result.append(item_new)
                else:
                    result.append(item)
            elif isinstance(item, ImageSegmentationData):
                # remove layers
                layers = self.remove_invalid_layers(item.annotation.layers)
                # no layers left? mark as negative
                if len(layers) == 0:
                    item_new = item.duplicate()
                    item_new.annotation = None
                    result.append(item_new)
                else:
                    item_new = item.duplicate()
                    item_new.annotation.layers = layers
                    result.append(item_new)
            else:
                self.logger().warning("Cannot process data type: %s" % str(type(item)))

        return flatten_list(result)
