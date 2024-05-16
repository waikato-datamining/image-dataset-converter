import math
import statistics
from typing import List

import shapely
from shapely import Polygon, MultiPolygon, LineString, distance
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Point as WaiPoint, Polygon as WaiPolygon

from ._objdet import LABEL_KEY, get_object_label, ObjectDetectionData

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


def merge_polygons(combined: ObjectDetectionData, max_slope_diff: float = 1e-6, max_dist: float = 1.0) -> ObjectDetectionData:
    """
    Merges adjacent polygons. Discards metadata apart from score, which it averages across merged objects,
    and the label, which has to be the same across objects.

    :param combined: the input data
    :type combined: ObjectDetectionData
    :param max_slope_diff: the maximum difference between slopes while still being considered parallel
    :type max_slope_diff: float
    :param max_dist: the maximum distance between parallel vertices
    :type max_dist: float
    :return: the (potentially) updated annotations
    :rtype: ObjectDetectionData
    """
    # for each polygon
    #   for each vertex in polygon
    #      compute slope
    # determine parallel vertices between objects
    # compute distance between parallel vertices
    # determine sets of objects to merge

    # determine vertices/slopes/intercepts
    vertices = dict()
    slopes = dict()
    normalized = combined.is_normalized()
    absolute = combined.get_absolute()
    for i in range(len(absolute)):
        vertices[i] = []
        slopes[i] = []
        if absolute[i].has_polygon():
            xs = absolute[i].get_polygon_x()
            ys = absolute[i].get_polygon_y()
        else:
            xs = [absolute[i].x, absolute[i].x + absolute[i].width - 1, absolute[i].x + absolute[i].width - 1, absolute[i].x]
            ys = [absolute[i].y, absolute[i].y, absolute[i].y + absolute[i].height - 1, absolute[i].y + absolute[i].height - 1]
        for n in range(len(xs)):
            # vertex: (x0,y0,x1,y1)
            vertices[i].append(LineString([(xs[n - 1], ys[n - 1]), (xs[n], ys[n])]))
            # slope: m = (y1-y0) / (x1-x0)
            if xs[n] - xs[n - 1] == 0:
                slope = math.inf
            else:
                slope = (ys[n] - ys[n - 1]) / (xs[n] - xs[n - 1])
            slopes[i].append(slope)

    # determine parallel vertices of objects with same label
    parallel = dict()
    for i in range(len(slopes)):
        label_i = get_object_label(absolute[i])
        for n in range(i + 1, len(slopes), 1):
            # only consider objects with the same label
            label_n = get_object_label(absolute[n])
            if label_i != label_n:
                continue
            for i_i in range(len(slopes[i])):
                for n_n in range(len(slopes[n])):
                    is_parallel = False

                    # horizontal lines
                    if (slopes[i][i_i] == 0) and (slopes[n][n_n] == 0):
                        is_parallel = True

                    # vertical lines
                    elif math.isinf(slopes[i][i_i]) and math.isinf(slopes[n][n_n]):
                        is_parallel = True

                    # compare slope
                    else:
                        slope_diff = abs(slopes[i][i_i] - slopes[n][n_n])
                        if slope_diff <= max_slope_diff:
                            is_parallel = True

                    # check distance of parallel vertices
                    if is_parallel:
                        d = distance(vertices[i][i_i], vertices[n][n_n])
                        if d <= max_dist:
                            if i not in parallel:
                                parallel[i] = set()
                            parallel[i].add(n)

    # create sets of objects to merge
    merge_sets = []
    to_merge = set()
    for i, ns in parallel.items():
        all_ = [i, *ns]
        found = None
        for a in all_:
            to_merge.add(a)
            for n, merge_set in enumerate(merge_sets):
                if a in merge_set:
                    found = n
                    break
            if found is not None:
                break
        if found is None:
            merge_sets.append(set(all_))
        else:
            for a in all_:
                merge_sets[found].add(a)

    if len(merge_sets) > 0:
        # transfer all objects that won't get merged
        annotation_new = LocatedObjects()
        for i, obj in enumerate(absolute):
            if i not in to_merge:
                annotation_new.append(obj)

        # merge sets
        for merge_set in merge_sets:
            label = None
            merged = None
            scores = []
            for i in merge_set:
                if label is None:
                    label = get_object_label(absolute[i])
                if "score" in absolute[i].metadata:
                    scores.append(float(absolute[i].metadata["score"]))
                if merged is None:
                    merged = locatedobject_polygon_to_shapely(absolute[i])
                else:
                    merged = shapely.union(merged, locatedobject_polygon_to_shapely(absolute[i]))
            obj = shapely_to_locatedobject(merged, label=label)
            # set average score
            if len(scores) > 0:
                score = statistics.mean(scores)
                obj.metadata["score"] = score
            annotation_new.append(obj)

        # update container
        combined.annotation = annotation_new
        if normalized:
            combined.to_normalized()

    return combined
