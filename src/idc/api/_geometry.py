from typing import List

from shapely import Polygon, MultiPolygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Point as WaiPoint, Polygon as WaiPolygon

from ._objdet import LABEL_KEY

UNION = "union"
INTERSECT = "intersect"
COMBINATIONS = [
    UNION,
    INTERSECT,
]


def locatedobject_bbox_to_shapely(lobj: LocatedObject) -> Polygon:
    """
    Converts the located object rectangle into a shapely Polygon.

    :param lobj: the bbox to convert
    :return: the Polygon
    """
    coords = [
        (lobj.x, lobj.y),
        (lobj.x + lobj.width - 1, lobj.y),
        (lobj.x + lobj.width - 1, lobj.y + lobj.height - 1),
        (lobj.x, lobj.y + lobj.height - 1),
        (lobj.x, lobj.y),
    ]
    return Polygon(coords)


def locatedobject_polygon_to_shapely(lobj: LocatedObject) -> Polygon:
    """
    Converts the located object polygon into a shapely Polygon.

    :param lobj: the polygon to convert
    :return: the Polygon
    """
    if not lobj.has_polygon():
        return locatedobject_bbox_to_shapely(lobj)
    x_list = lobj.get_polygon_x()
    y_list = lobj.get_polygon_y()
    coords = []
    for x, y in zip(x_list, y_list):
        coords.append((x, y))
    coords.append((x_list[0], y_list[0]))
    return Polygon(coords)


def shapely_to_locatedobject(geometry: BaseGeometry, label: str = None) -> LocatedObject:
    """
    Turns the shapely geometry back into a located object.
    Assumes absolute coordinates.

    :param geometry: the geometry to convert
    :type geometry: BaseGeometry
    :param label: the label to set (when not None)
    :type label: str
    :return: the generated object
    :rtype: LocatedObject
    """
    # use convex hull in case of MultiPolygon
    if isinstance(geometry, MultiPolygon):
        geometry = geometry.convex_hull

    minx, miny, maxx, maxy = geometry.bounds
    result = LocatedObject(minx, miny, maxx-minx+1, maxy-miny+1)
    if label is not None:
        result.metadata[LABEL_KEY] = label

    if isinstance(geometry, Polygon):
        x_list, y_list = geometry.exterior.coords.xy
        points = []
        for i in range(len(x_list)):
            points.append(WaiPoint(x=x_list[i], y=y_list[i]))
        result.set_polygon(WaiPolygon(*points))

    return result


def locatedobjects_to_shapely(located_objects: LocatedObjects) -> List[Polygon]:
    """
    Turns the located objects into shapely polygons.

    :param located_objects: the objects to convert
    :type located_objects: LocatedObjects
    :return: the list of polygons
    :rtype: list
    """
    result = []
    for obj in located_objects:
        result.append(locatedobject_polygon_to_shapely(obj))
    return result


def intersect_over_union(poly1: Polygon, poly2: Polygon) -> float:
    """
    Calculates the IoU (intersect over union) for the two polygons.

    :param poly1: the first polygon
    :type poly1: Polygon
    :param poly2: the second polygon
    :type poly2: Polygon
    :return: the IoU
    :type: float
    """
    try:
        intersection = poly2.intersection(poly1)
        if intersection.area > 0:
            union = unary_union([poly2, poly1])
            return intersection.area / union.area
        else:
            return 0
    except:
        print("Failed to compute IoU!")
        return 0
