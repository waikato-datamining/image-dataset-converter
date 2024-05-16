import argparse
import re
from typing import List

from seppl.io import Filter
from shapely.geometry import Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, locatedobject_polygon_to_shapely, intersect_over_union, get_object_label, flatten_list, make_list


class LabelPresent(Filter):
    """
    Only forwards images that have the specified label(s) present.
    """

    def __init__(self, labels: List[str] = None, regexp: str = None, region: str = None,
                 coordinate_separator: str = ";", pair_separator: str = ",", min_iou: float = None,
                 invert_regions: bool = False, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param labels: the labels to use
        :type labels: list
        :param regexp: the regular expression for using only a subset
        :type regexp: str
        :param region: list of x/y pairs defining the region that the object must overlap with in order to be included. Values between 0-1 are considered normalized, otherwise absolute pixels.
        :type region: str
        :param coordinate_separator: the separator between coordinates
        :type coordinate_separator: str
        :param pair_separator: the separator between coordinates
        :type pair_separator: str
        :param min_iou: the minimum IoU (intersect over union) that the object must have with the region in order to be considered an overlap (object detection only)
        :type min_iou: float
        :param invert_regions: Inverts the matching sense from 'labels have to overlap at least one of the region(s)' to 'labels cannot overlap any region'
        :type invert_regions: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.labels = labels
        self.regexp = regexp
        self.region = region
        self.coordinate_separator = coordinate_separator
        self.pair_separator = pair_separator
        self.min_iou = min_iou
        self.invert_regions = invert_regions
        self._pattern = None
        self._regions = None
        self._normalized = None
        self._polygons = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "label-present"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Only forwards images that have the specified label(s) present."

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
        return [ObjectDetectionData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--labels", type=str, default=None, help="The labels to use", required=False, nargs="*")
        parser.add_argument("--regexp", type=str, default=None, help="Regular expression for using only a subset of labels", required=False)
        parser.add_argument("--region", type=str, default=None, help="List of x/y pairs defining the region that the object must overlap with in order to be included. Values between 0-1 are considered normalized, otherwise absolute pixels.", required=False)
        parser.add_argument("--coordinate_separator", type=str, default=";", help="the separator between coordinates", required=False)
        parser.add_argument("--pair_separator", type=str, default=",", help="the separator between the x and y of a pair", required=False)
        parser.add_argument("--min_iou", type=float, default=None, help="The minimum IoU (intersect over union) that the object must have with the region in order to be considered an overlap (object detection only)", required=False)
        parser.add_argument("--invert_regions", action="store_true", help="Inverts the matching sense from 'labels have to overlap at least one of the region(s)' to 'labels cannot overlap any region'", required=False)
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
        self.coordinate_separator = ns.coordinate_separator
        self.pair_separator = ns.pair_separator
        self.min_iou = ns.min_iou
        self.invert_regions = ns.invert_regions

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._pattern = re.compile(self.regexp) if (self.regexp is not None) else None

        if len(self.coordinate_separator) != 1:
            raise Exception("Coordinate separator must be a single character, but found: %s" % self.coordinate_separator)
        if len(self.pair_separator) != 1:
            raise Exception("Pair separator must be a single character, but found: %s" % self.pair_separator)

        self._regions = []
        self._normalized = True
        self._polygons = {}
        if self.region is not None:
            for r in self.region:
                region = []
                coords = r.split(self.coordinate_separator)
                if len(coords) < 3:
                    raise Exception("Region must have at least three coordinates of format 'x,y' separated by '%s', but found: %s" % (self.coordinate_separator, r))
                for coord in coords:
                    pair = coord.split(self.pair_separator)
                    if len(pair) != 2:
                        raise Exception("Coordinates must have format 'x%sy', but found '%s' in region '%s'!" % (self.pair_separator, coord, r))
                    region.append([float(x) for x in pair])
                self._regions.append(region)
                # not normalized?
                if sum([(0 if (sum(x) < 2) else 1) for x in region]) > 0:
                    self._normalized = False

    def check_label(self, label: str) -> bool:
        """
        Checks whether the label fits the criteria.

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

    def check_regions(self, located_object: LocatedObject, width: int, height: int) -> bool:
        """
        Checks whether the object falls within at least one of the regions or, when inverting,
        whether it does not fall within any.

        :param located_object: the object to check
        :param width: the width of the image
        :param height: the height of the image
        :return: True if no regions defined or if object matches at least one region (invert_regions=False) or none at all (invert_regions=True)
        """
        if len(self._regions) == 0:
            return True

        key = "%d-%d" % (width, height)

        # already created polygons for image dimensions?
        if key not in self._polygons:
            region_polys = []
            self._polygons[key] = region_polys
            for region in self._regions:
                if self._normalized:
                    points = []
                    for x, y in region:
                        points.append([int(x * width), int(y * height)])
                else:
                    points = region
                region_polys.append(Polygon(points))
        else:
            region_polys = self._polygons[key]

        # overlap with any region?
        object_poly = locatedobject_polygon_to_shapely(located_object)
        match = False
        for region_poly in region_polys:
            iou = intersect_over_union(object_poly, region_poly)
            self.logger().debug("object_poly: %s" % str(object_poly))
            self.logger().debug("region_poly: %s" % str(region_poly))
            self.logger().debug("iou: %f > %f = %s" % (iou, self.min_iou, str(iou > self.min_iou)))
            if iou > self.min_iou:
                match = True
                break

        result = (not self.invert_regions and match) or (self.invert_regions and not match)
        self.logger().debug("check_regions = %s" % str(result))
        return result

    def find_valid_objects(self, located_objects: LocatedObjects, width: int, height: int) -> List[int]:
        """
        Returns indices of objects that match the search criteria.

        :param located_objects: The located objects to process.
        :param width: the width of the image
        :param height: the height of the image
        :return: the list of indices of objects matching the criteria
        """
        result = []

        # Search the located objects
        for index, located_object in enumerate(located_objects):
            label = get_object_label(located_object)
            label_ok = self.check_label(label)
            self.logger().debug("check_label: %s = %s" % (label, str(label_ok)))
            if label_ok:
                if self.check_regions(located_object, width, height):
                    result.append(index)

        return result

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            # determines annotations that match criteria
            indices = self.find_valid_objects(item.get_absolute(), item.image_width, item.image_height)
            self.logger().debug("indices: %s" % str(indices))
            if len(indices) > 0:
                result.append(item)
            else:
                self.logger().info("Discarding: %s" % item.image_name)

        return flatten_list(result)
