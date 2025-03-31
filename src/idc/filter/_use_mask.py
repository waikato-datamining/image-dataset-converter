import argparse
import os.path
from typing import List

from seppl.io import Filter
from simple_palette_utils import generate_palette_list, PALETTE_AUTO, palettes
from wai.logging import LOGGING_WARNING

from idc.api import DATATYPES, data_type_to_class, ImageData, to_indexedpng
from idc.api import ImageSegmentationData, flatten_list, make_list


class UseMask(Filter):
    """
    Uses the images segmentation annotations (= mask) as the new base image.
    """

    def __init__(self, data_type: str = None, palette: str = None, use_rgb: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param data_type: the type of output to generate with the mask
        :type data_type: str
        :param palette: the palette to use, either a supported palette name (auto|x11|light|dark) or comma-separated list of R,G,B values
        :type palette: str
        :param use_rgb: whether to use RGB mode rather than palette mode
        :type use_rgb: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.data_type = data_type
        self.palette = palette
        self.use_rgb = use_rgb
        self._output_cls = None
        self._palette_list = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "use-mask"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Uses the images segmentation annotations (= mask) as the new base image."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageSegmentationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self.data_type is None:
            return [ImageData]
        else:
            return [data_type_to_class(self.data_type)]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-t", "--data_type", choices=DATATYPES, type=str, default=None, help="The type of data to forward", required=True)
        parser.add_argument("-p", "--palette", metavar="PALETTE", type=str, default=PALETTE_AUTO, help="The palette to use; either palette name (%s) or comma-separated list of R,G,B values." % "|".join(palettes()), required=False)
        parser.add_argument("--use_rgb", action="store_true", help="Whether to force RGB mode instead of palette mode.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.data_type = ns.data_type
        self.palette = ns.palette
        self.use_rgb = ns.use_rgb

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.data_type is None:
            raise Exception("No data type defined!")
        self._palette_list = generate_palette_list(self.palette)
        self._output_cls = data_type_to_class(self.data_type)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if item.has_annotation():
                new_image_name = os.path.splitext(item.image_name)[0] + ".png"
                new_image = to_indexedpng(item.image_width, item.image_height, item.annotation, self._palette_list, background=0)
                if self.use_rgb:
                    new_image = new_image.convert("RGB")
                new_item = self._output_cls(image_name=new_image_name, image=new_image)
                result.append(new_item)

        return flatten_list(result)
