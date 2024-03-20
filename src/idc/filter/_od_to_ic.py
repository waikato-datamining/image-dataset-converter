import argparse
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import ObjectDetectionData, ImageClassificationData, flatten_list, make_list, get_object_label


MULTIPLICITY_ERROR = "error"
MULTIPLICITY_MAJORITY = "majority"
MULTIPLICITY_SINGLE = "single"
MULTIPLICITY_SKIP = "skip"
MULTIPLICITY = [
    MULTIPLICITY_ERROR,
    MULTIPLICITY_MAJORITY,
    MULTIPLICITY_SINGLE,
    MULTIPLICITY_SKIP,
]


class ObjectDetectionToImageClassification(Filter):
    """
    Converts object detection annotations into image classification ones.
    """

    def __init__(self, multiplicity: str = MULTIPLICITY_ERROR,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param multiplicity: how to handle instances with more than one located object
        :type multiplicity: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.multiplicity = multiplicity

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "od-to-ic"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Converts object detection annotations into image classification ones."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--multiplicity", choices=MULTIPLICITY, default=MULTIPLICITY_ERROR, help="How to handle instances with more than one located object", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.multiplicity = ns.multiplicity

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            ann = item.annotation
            if (ann is None) or (len(ann) == 0):
                item_new = ImageClassificationData(source=item.source, image=item.image, data=item.data, metadata=item.get_metadata())
            else:
                if len(ann) > 1:
                    if self.multiplicity == "error":
                        raise Exception("More than one detected object for: %s" % item.image_name)
                    elif self.multiplicity == "skip":
                        return
                    elif self.multiplicity == "single":
                        labels = set(map(get_object_label, ann))
                        if len(labels) > 1:
                            raise Exception("More than one type of detected object for: %s" % item.image_name)
                        label = labels.pop()
                    elif self.multiplicity == "majority":
                        labels = {}
                        for label in map(get_object_label, ann):
                            if label in labels:
                                labels[label] += 1
                            else:
                                labels[label] = 1
                        label = max(labels.keys(), key=labels.get)
                    else:
                        raise Exception("Unhandled multiplicity: %s" % self.multiplicity)
                else:
                    label = get_object_label(ann[0])
                item_new = ImageClassificationData(source=item.source, image=item.image, data=item.data, metadata=item.get_metadata(), annotation=label)

            result.append(item_new)

        return flatten_list(result)
