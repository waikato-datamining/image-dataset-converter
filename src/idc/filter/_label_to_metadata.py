import argparse
from typing import List, Dict, Optional

from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageClassificationData, ImageSegmentationData, get_object_label, \
    flatten_list, make_list, safe_deepcopy


class LabelToMetaData(Filter):
    """
    Stores labels in meta-data.
    """

    def __init__(self, metadata_key: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param metadata_key: the metadata key to store the label under
        :type metadata_key: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.metadata_key = metadata_key

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "label-to-metadata"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Stores labels in meta-data. In case of object detection and image segmentation, a copy of the data is forwarded for each unique label."

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
        parser.add_argument("-k", "--metadata_key", type=str, help="The key in the meta-data to store the label under.", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.metadata_key = ns.metadata_key

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.metadata_key is None:
            raise Exception("No meta-data key provided!")

    def _update_metadata(self, meta: Optional[Dict], label: str) -> Dict:
        """
        Updates the meta-data dictionary and returns it.

        :param meta: the meta-data dictionary to update, can be None
        :type meta: dict
        :param label: the label to store
        :type label: str
        :return: the new meta-data dictionary
        :rtype: dict
        """
        if meta is None:
            result = dict()
        else:
            result = safe_deepcopy(meta)
        result[self.metadata_key] = label
        self.logger().info("%s = %s" % (self.metadata_key, label))
        return result

    def _process_image_classification(self, current: ImageClassificationData, items: List):
        """
        Processes the image classification data.

        :param current: the item to process
        :type current: ObjectDetectionData
        :param items: the list to add the new items to
        :type items: list
        """
        # If the object doesn't have a label, skip it
        if current.annotation is None:
            return
        new_item = safe_deepcopy(current)
        new_item.set_metadata(self._update_metadata(new_item.get_metadata(), current.annotation))
        items.append(new_item)

    def _process_object_detection(self, current: ObjectDetectionData, items: List):
        """
        Processes the object detection data.

        :param current: the item to process
        :type current: ObjectDetectionData
        :param items: the list to add the new items to
        :type items: list
        """
        labels = set()
        for located_object in current.annotation:
            # Get the object's current label
            label = get_object_label(located_object, default_label=None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # already processed label?
            if label in labels:
                continue

            labels.add(label)
            new_item = safe_deepcopy(current)
            new_item.set_metadata(self._update_metadata(new_item.get_metadata(), label))
            items.append(new_item)

    def _process_image_segmentation(self, current: ImageSegmentationData, items: List):
        """
        Processes the image segmentation data.

        :param current: the item to process
        :type current: ImageSegmentationData
        :param items: the list to add the new items to
        :type items: list
        """
        labels = set()
        for label in current.annotation.layers:
            # already processed label?
            if label in labels:
                continue

            labels.add(label)
            new_item = safe_deepcopy(current)
            new_item.set_metadata(self._update_metadata(new_item.get_metadata(), label))
            items.append(new_item)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if item.has_annotation():
                if isinstance(item, ImageClassificationData):
                    self._process_image_classification(item, result)
                elif isinstance(item, ObjectDetectionData):
                    self._process_object_detection(item, result)
                elif isinstance(item, ImageSegmentationData):
                    self._process_image_segmentation(item, result)
                else:
                    self.logger().warning("Cannot process data type: %s" % str(type(item)))

        return flatten_list(result)
