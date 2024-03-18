from shapely.geometry import Polygon
from shapely.ops import unary_union

UNION = "union"
INTERSECT = "intersect"
COMBINATIONS = [
    UNION,
    INTERSECT,
]


def to_polygon(located_object):
    """
    Turns the located object into a shapely polygon.

    :param located_object: the object to convert
    :type located_object: LocatedObject
    :return: the generated polygon object
    :rtype: Polygon
    """
    coords = []
    for point in located_object.get_polygon().points:
        coords.append((point.x, point.y))
    return Polygon(coords)


def to_polygons(located_objects):
    """
    Turns the located objects into shapely polygons.

    :param located_objects: the objects to convert
    :type located_objects: LocatedObjects
    :return: the list of polygons
    :rtype: list
    """
    result = []
    for obj in located_objects:
        result.append(to_polygon(obj))
    return result


def intersect_over_union(poly1, poly2):
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
