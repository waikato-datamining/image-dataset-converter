import argparse
import glob
import os.path
from typing import List, Iterable, Union

import numpy as np
from PIL import Image, ImageOps
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from wai.logging import LOGGING_WARNING

from idc.api import ImageSegmentationData, ImageSegmentationAnnotations
from idc.api import Reader


class LayerSegmentsImageSegmentationReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 label_separator: str = "-", labels: List[str] = None,
                 lenient: bool = False, invert: bool = False,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param label_separator: the separator between name and label for the masks
        :type label_separator: str
        :param labels: the list of labels
        :type labels: list
        :param lenient: whether to quietly convert non-binary images with just two unique colors into binary ones or raise an exception
        :type lenient: bool
        :param invert: whether to invert the binary images (b/w <-> w/b)
        :type invert: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.label_separator = label_separator
        self.labels = labels
        self.lenient = lenient
        self.invert = invert
        self._label_mapping = None
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-layer-segments-is"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the annotations from associated mask PNG image files, with one binary mask per layer/label."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the JPG file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the JPG files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--labels", metavar="LABEL", type=str, default=None, help="The labels that the indices represent.", nargs="+")
        parser.add_argument("--label_separator", type=str, help="The separator between name and label used by the mask images.", required=False, default="-")
        parser.add_argument("--lenient", action="store_true", help="Will convert non-binary masks with just two unique color values quietly to binary without raising an exception.")
        parser.add_argument("--invert", action="store_true", help="Will invert the binary images (b/w <-> w/b).")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.labels = ns.labels
        self.label_separator = ns.label_separator
        self.lenient = ns.lenient
        self.invert = ns.invert

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ImageSegmentationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.labels is None:
            raise Exception("No labels defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.jpg")

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input

        # associated layers?
        prefix = os.path.splitext(self.session.current_input)[0]
        anns = glob.glob(prefix + self.label_separator + "*.png")
        if len(anns) == 0:
            self.logger().warning("No associated layers found for: %s" % self.session.current_input)
            self._current_input = None
            yield None

        # read annotations
        prefix_short = os.path.basename(prefix)
        layers = dict()
        for ann in anns:
            self.logger().info("Reading from: " + str(ann))
            ann_short = os.path.splitext(os.path.basename(ann))[0]
            label = ann_short[len(prefix_short + self.label_separator):]
            if label in self.labels:
                img = Image.open(ann)
                if img.mode != "1":
                    arr = np.asarray(img).astype(np.uint8)
                    unique = np.unique(arr)
                    if self.lenient and (len(unique) == 2):
                        for i in range(2):
                            arr = np.where(arr == unique[i], i*255, arr)
                        img = Image.fromarray(arr, "L").convert("1")
                    else:
                        raise Exception("Layer mask is not binary: %s! Try using --lenient flag to attempt loading file(s)." % ann)
                if self.invert:
                    img = ImageOps.invert(img)
                arr = np.asarray(img).astype(np.uint8)
                arr = np.where(arr == 1, 255, arr).astype(np.uint8)
                layers[label] = arr
            else:
                self.logger().warning("Skipping unknown label: %s" % label)

        annotations = ImageSegmentationAnnotations(self.labels, layers)
        yield ImageSegmentationData(source=self.session.current_input, annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
