import argparse
from typing import List, Iterable, Union

from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from wai.logging import LOGGING_WARNING

from kasperl.api import locate_file, Reader, AnnotationsOnlyReader, add_annotations_only_reader_param, annotation_to_name
from idc.api import ImageSegmentationData, load_image_from_file, imgseg_from_bluechannel, JPEG_EXTENSIONS, empty_image, FORMAT_JPEG, FORMAT_EXTENSIONS


class BlueChannelImageSegmentationReader(Reader, PlaceholderSupporter, AnnotationsOnlyReader):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 image_path_rel: str = None, labels: List[str] = None, background: int = None, resume_from: str = None,
                 annotations_only: bool = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param image_path_rel: the relative path from the annotations to the images
        :type image_path_rel: str
        :param labels: the list of labels
        :type labels: list
        :param background: the index (0-255) that is used as background
        :type background: int
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param annotations_only: whether to only load the annotations
        :type annotations_only: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.image_path_rel = image_path_rel
        self.labels = labels
        self.background = background
        self.resume_from = resume_from
        self.annotations_only = annotations_only
        self._label_mapping = None
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-blue-channel-is"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the annotations from associated blue channel PNG files. When reading only the annotations, an empty image of the same dimensions is used."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the PNG file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the PNG files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.png'", required=False)
        parser.add_argument("--image_path_rel", metavar="PATH", type=str, default=None, help="The relative path from the annotations to the images directory", required=False)
        parser.add_argument("--labels", metavar="LABEL", type=str, default=None, help="The labels that the indices represent.", nargs="+")
        parser.add_argument("--background", type=int, help="The index (0-255) that is used for the background", required=False, default=0)
        add_annotations_only_reader_param(parser)
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
        self.image_path_rel = ns.image_path_rel
        self.labels = ns.labels
        self.background = ns.background
        self.resume_from = ns.resume_from
        self.annotations_only = ns.annotations_only

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
        self._inputs = None
        self._label_mapping = dict()
        for i, label in enumerate(self.labels):
            self._label_mapping[i] = label
        self.logger().debug("label mapping: %s" % str(self._label_mapping))
        if self.annotations_only is None:
            self.annotations_only = False

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        if self._inputs is None:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.png", resume_from=self.resume_from)
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input

        # associated images?
        imgs = []
        if not self.annotations_only:
            imgs = locate_file(self.session.current_input, JPEG_EXTENSIONS, rel_path=self.image_path_rel)
            if len(imgs) == 0:
                self.logger().warning("Failed to locate associated image for: %s" % self.session.current_input)
                yield None

        # read annotations
        self.logger().info("Reading from: " + str(self.session.current_input))
        ann = load_image_from_file(self.session.current_input)
        annotations = imgseg_from_bluechannel(ann, self.labels, self._label_mapping, self.logger(), background=self.background)

        # associated image
        if not self.annotations_only:
            if len(imgs) > 1:
                self.logger().warning("Found more than one image associated with annotation, using first: %s" % imgs[0])
                yield None
            yield ImageSegmentationData(source=imgs[0], annotation=annotations)
        else:
            image_name = annotation_to_name(self.session.current_input, ext=FORMAT_EXTENSIONS[FORMAT_JPEG])
            image, _ = empty_image("RGB", ann.size[0], ann.size[1], FORMAT_JPEG)
            yield ImageSegmentationData(image_name=image_name, image=image, image_format=FORMAT_JPEG, annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return (self._inputs is not None) and len(self._inputs) == 0
