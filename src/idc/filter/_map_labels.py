import argparse
import copy
import numpy as np
import re
from typing import List, Union, Optional

from seppl.io import BatchFilter
from wai.common.adams.imaging.locateobjects import LocatedObjects, NormalizedLocatedObjects
from wai.logging import LOGGING_WARNING

from kasperl.api import make_list, flatten_list
from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, get_object_label, \
    set_object_label, ImageSegmentationAnnotations


class MapLabels(BatchFilter):
    """
    Filters out labels according to the parameters.
    """

    def __init__(self, mapping: List[str] = None,
                 old_labels: List[str] = None, old_regexps: List[str] = None, new_label: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mapping: the label mapping to use (list of old=new pairs), ignored if None
        :type mapping: list
        :param old_labels: the list of old labels to map to the new one, requires new_label
        :type old_labels: str
        :param old_regexps: the list of regexps for matching the old labels and mapping to the new one, requires new_label
        :type old_regexps: str
        :param new_label: the new label to map to, requires old_labels and/or old_regexp
        :type new_label: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.mapping = mapping
        self.old_labels = old_labels
        self.old_regexps = old_regexps
        self.new_label = new_label
        self._mapping = None
        self._regexps = None

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
        return "Maps labels from one set to another. In case of image-segmentation, layers may get merged."

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
        parser.add_argument("-o", "--old_labels", type=str, metavar="LABEL", default=None, help="The old labels to replace with the new one, requires -n/--new_label", required=False, nargs="*")
        parser.add_argument("-O", "--old_regexps", type=str, metavar="REGEXP", default=None, help="The regexps for matching the old labels to replace with the new one, requires -n/--new_label", required=False, nargs="*")
        parser.add_argument("-n", "--new_label", type=str, metavar="LABEL", default=None, help="The new label to use", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.mapping = ns.mapping
        self.old_labels = ns.old_labels
        self.old_regexps = ns.old_regexps
        self.new_label = ns.new_label

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._mapping = {}
        if self.mapping is not None:
            for map_string in self.mapping:
                old, new = map_string.split("=")
                # Make sure we don't double-map a label
                if old in self._mapping:
                    raise ValueError(f"Multiple mappings specified for label '%s': %s, %s" % (old, self._mapping[old], new))
                self._mapping[old] = new
        if self.new_label is not None:
            if self.old_labels is not None:
                for old in self.old_labels:
                    self._mapping[old] = self.new_label
            if self.old_regexps is not None:
                self._regexps = []
                for old in self.old_regexps:
                    self._regexps.append(re.compile(old))

    def _can_replace(self):
        """
        Whether labels can be replaced at all.

        :return: True if labels can be replaced
        :rtype: bool
        """
        return (len(self._mapping) > 0) or (len(self._regexps) > 0)

    def _matches(self, label: str) -> bool:
        """
        Checks whether the label has a mapping.

        :param label: the label to check
        :type label: str
        :return: True if a mapping exists
        :rtype: bool
        """
        if label is None:
            return False
        if label in self._mapping:
            return True
        if self._regexps is not None:
            for regexp in self._regexps:
                if regexp.match(label) is not None:
                    return True
        return False

    def _replace(self, label: Optional[str]) -> Optional[str]:
        """
        Replaces the old label with the new one.

        :param label: the label to update, can be None
        :type label: str or None
        :return: the updated label
        :rtype: str or None
        """
        if label is None:
            return label
        if label in self._mapping:
            return self._mapping[label]
        if self._regexps is not None:
            for regexp in self._regexps:
                if regexp.match(label) is not None:
                    return self.new_label
        return label

    def process_object_detection(self, annotation: Union[LocatedObjects, NormalizedLocatedObjects]) -> bool:
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param annotation: The parsed objects
        :return: whether updated
        :rtype: bool
        """
        # Process each object
        result = False
        for located_object in annotation:
            # Get the object's current label
            label = get_object_label(located_object, default_label=None)

            # only update if we have a match
            if self._matches(label):
                set_object_label(located_object, self._replace(label))
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

        # update list of possible labels
        new_labels = set()
        label_list = list(annotation.labels)
        for label in label_list:
            if self._matches(label):
                new_label = self._replace(label)
                if new_label == label:
                    continue
                new_labels.add(new_label)
                i = annotation.labels.index(label)
                if new_label in annotation.labels:
                    annotation.labels.pop(i)
                else:
                    annotation.labels[i] = new_label
                result = True

        # ensure that all new labels are present in list of labels
        for new_label in new_labels:
            if new_label not in annotation.labels:
                annotation.labels.append(new_label)
                result = True

        # update layers, merge if necessary
        label_list = list(annotation.layers.keys())
        for label in label_list:
            if self._matches(label):
                new_label = self._replace(label)
                data = annotation.layers[label]
                del annotation.layers[label]
                # if layer already present, merge
                if new_label in annotation.layers:
                    np.copyto(annotation.layers[new_label], data, 'safe', data > 0)
                else:
                    annotation.layers[new_label] = data
                result = True

        return result

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        # Do nothing if no mapping provided
        if not self._can_replace():
            return data

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
                    if self._matches(item.annotation):
                        item_new = item.duplicate(annotation=self._replace(item.annotation))

                elif isinstance(item, ImageSegmentationData):
                    ann_new = copy.deepcopy(item.annotation)
                    updated = self.process_image_segmentation(ann_new)
                    if updated:
                        item_new = item.duplicate(annotation=ann_new)
                else:
                    self.logger().warning("Cannot process data type: %s" % str(type(item)))
            result.append(item_new)

        return flatten_list(result)
