import argparse
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from wai.common.geometry import NormalizedPoint, NormalizedPolygon
from wai.common.adams.imaging.locateobjects import NormalizedLocatedObjects, NormalizedLocatedObject
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from idc.api import ObjectDetectionData, locate_image, Reader, load_labels


class YoloObjectDetectionReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 image_path_rel: str = None, use_polygon_format: bool = False, labels: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param image_path_rel: the relative path from the annotations to the images
        :type image_path_rel: str
        :param use_polygon_format: whether to use the polygon format
        :type use_polygon_format: bool
        :param labels: the text file with the comma-separated list of labels
        :type labels: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.image_path_rel = image_path_rel
        self.use_polygon_format = use_polygon_format
        self.labels = labels
        self._label_mapping = None
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-yolo-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box and/or polygon definitions from the associated .txt file in YOLO format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the text file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the text files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--image_path_rel", metavar="PATH", type=str, default=None, help="The relative path from the annotations to the images directory", required=False)
        parser.add_argument("-p", "--use_polygon_format", action="store_true", help="Whether to read the annotations in polygon format rather than bbox format", required=False)
        parser.add_argument("--labels", metavar="FILE", type=str, default=None, help="The text file with the comma-separated list of labels", required=False)
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
        self.use_polygon_format = ns.use_polygon_format
        self.labels = ns.labels

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.image_path_rel is None:
            self.image_path_rel = "../images"
        if self.labels is None:
            raise Exception("No labels file defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.txt")
        _, self._label_mapping = load_labels(self.labels, logger=self.logger())

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        with open(self.session.current_input, "r") as fp:
            lines = fp.readlines()
            lines = [x.strip() for x in lines]

        annotations = NormalizedLocatedObjects()
        for line in lines:
            if len(line) == 0:
                continue
            parts = line.split(" ")
            if len(parts) < 3:
                continue
            label = int(parts[0])
            meta = {"type": self._label_mapping[label]}
            parts = parts[1:]
            if self.use_polygon_format:
                if len(parts) % 2 != 0:
                    self.logger().warning("Cannot process uneven number of coordinates in polygon format: %s" % line)
                    continue
                points = []
                minx = 1.0
                maxx = 0.0
                miny = 1.0
                maxy = 0.0
                for i in range(len(parts) // 2):
                    x = float(parts[i*2])
                    y = float(parts[i*2+1])
                    point = NormalizedPoint(x, y)
                    points.append(point)
                    minx = min(minx, x)
                    maxx = max(maxx, x)
                    miny = min(miny, y)
                    maxy = max(maxy, y)
                poly = NormalizedPolygon(*points)
                obj = NormalizedLocatedObject(minx, miny, (maxx - minx), (maxy - miny), **meta)
                obj.set_polygon(poly)
                annotations.append(obj)
            else:
                if len(parts) != 4:
                    self.logger().warning("BBox format requires 4 values (left, top, width, height), but got %d instead: %s" % (len(parts), line))
                    continue
                x_center = float(parts[0])
                y_center = float(parts[1])
                width = float(parts[2])
                height = float(parts[3])
                obj = NormalizedLocatedObject(x_center - width / 2, y_center - height / 2, width, height, **meta)
                annotations.append(obj)

        image = locate_image(self._current_input, rel_path=self.image_path_rel)
        if image is None:
            self.logger().warning("No associated image found: %s" % self._current_input)
            yield None

        yield ObjectDetectionData(source=image, annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
