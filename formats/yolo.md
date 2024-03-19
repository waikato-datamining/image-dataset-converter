# YOLO

YOLO annotations are stored in `.txt` files. There are two different sub-formats available:
* bounding box format
* polygon format

## Bounding box format

The bounding box format has one line per annotation, using the following format:

```
class x_center y_center width height
```

The coordinates and dimensions are normalized (0-1) rather than absolute.

## Polygon format

In order to accommodate mask/shape detection, a variant for managing polygons was 
introduced later, using this format:

```
class x0 y0 x1 y1 x2 y2 ...
```

The x/y coordinates are normalized as well (0-1).
