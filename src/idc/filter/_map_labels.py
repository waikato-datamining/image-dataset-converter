import argparse
import copy
from typing import List, Union

from seppl.io import Filter
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, get_object_label, \
    set_object_label, ImageSegmentationAnnotations, flatten_list, make_list


class MapLabels(Filter):
    """
    Filters out labels according to the parameters.
    """

    def __init__(self, mapping: List[str] = None, 
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mapping: the label mapping to use (list of old=new pairs)
        :type mapping: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.mapping = mapping
        self._mapping = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "map-labels"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Maps labels from one set to another."

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
        parser.add_argument("-m", "--mapping", type=str, metavar="old=new", default=None, help="The labels to use", required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.mapping = ns.mapping

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._mapping = {}
        for map_string in self.mapping:
            old, new = map_string.split("=")
            # Make sure we don't double-map a label
            if old in self._mapping:
                raise ValueError(f"Multiple mappings specified for label '%s': %s, %s" % (old, self._mapping[old], new))
            self._mapping[old] = new

    def process_object_detection(self, annotation: Union[LocatedObjects, NormalizedLocatedObjects]) -> bool:
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param annotation: The parsed objects
        :return: whether updated
        :rtype: bool
        """
        # Do nothing if no mapping provided
        if len(self._mapping) == 0:
            return False

        # Process each object
        result = False
        for located_object in annotation:
            # Get the object's current label
            label = get_object_label(located_object, default_label=None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self._mapping:
                set_object_label(located_object, self._mapping[label])
                result = True

        return result

    def process_image_segmentation(self, annotation: ImageSegmentationAnnotations) -> bool:
        """
        Processes the image segmentation annotations.

        :param annotation: the annotations to process
        :type annotation: ImageSegmentationAnnotations
        :return: whether the annotations were updated
        :rtype: bool
        """
        result = False

        for label in self._mapping:
            if label in annotation.labels:
                i = annotation.labels.index(label)
                annotation.labels[i] = self._mapping[label]
                result = True
            if label in annotation.layers:
                data = annotation.layers[label]
                del annotation.layers[label]
                annotation.layers[self._mapping[label]] = data
                result = True

        return result

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            item_new = item
            if item.has_annotation():
                if isinstance(item, ObjectDetectionData):
                    ann_new = copy.deepcopy(item.annotation)
                    updated = self.process_object_detection(ann_new)
                    if updated:
                        item_new = item.duplicate(annotation=ann_new)
                elif isinstance(item, ImageClassificationData):
                    if item.annotation in self._mapping:
                        item_new = item.duplicate(annotation=self._mapping[item.annotation])
                elif isinstance(item, ImageSegmentationData):
                    ann_new = copy.deepcopy(item.annotation)
                    updated = self.process_image_segmentation(ann_new)
                    if updated:
                        item_new = item.duplicate(annotation=ann_new)
                else:
                    self.logger().warning("Cannot process data type: %s" % str(type(item)))
            result.append(item_new)

        return flatten_list(result)
