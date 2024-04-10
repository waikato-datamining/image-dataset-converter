import argparse
import copy
from typing import List, Union

from seppl.io import Filter
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, ImageSegmentationAnnotations, \
    get_object_label, flatten_list, make_list


class RemoveClasses(Filter):
    """
    Removes the specified classes/labels.
    """

    def __init__(self, classes: List[str] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param classes: the classes/labels to remove
        :type classes: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.classes = classes

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "remove-classes"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Removes the specified classes/labels."

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
        parser.add_argument("--classes", type=str, default=None, help="The classes/labels to remove", required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.classes = ns.classes

    def process_object_detection(self, annotation: Union[LocatedObjects, NormalizedLocatedObjects]) -> bool:
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param annotation: The parsed objects
        :return: whether updated
        :rtype: bool
        """
        # Do nothing if no mapping provided
        if len(self.classes) == 0:
            return False

        # Process each object
        delete = []
        for i, located_object in enumerate(annotation):
            # Get the object's current label
            label = get_object_label(located_object, default_label=None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self.classes:
                delete.append(i)
        delete = sorted(delete, reverse=True)

        # remove objects
        result = False
        for i in delete:
            result = True
            annotation.pop(i)

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

        for label in self.classes:
            if label in annotation.labels:
                annotation.labels.remove(label)
                result = True
            if label in annotation.layers:
                del annotation.layers[label]
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
                if isinstance(item, ImageClassificationData):
                    if item.annotation in self.classes:
                        # skip item
                        continue
                elif isinstance(item, ObjectDetectionData):
                    ann_new = copy.deepcopy(item.annotation)
                    updated = self.process_object_detection(ann_new)
                    if updated:
                        item_new = item.duplicate(annotation=ann_new)
                elif isinstance(item, ImageSegmentationData):
                    ann_new = copy.deepcopy(item.annotation)
                    updated = self.process_image_segmentation(ann_new)
                    if updated:
                        item_new = item.duplicate(annotation=ann_new)
                else:
                    self.logger().warning("Cannot process data type: %s" % str(type(item)))
            result.append(item_new)

        return flatten_list(result)
