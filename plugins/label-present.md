# label-present

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Only forwards images that have the specified label(s) present.

```
usage: label-present [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [--labels [LABELS [LABELS ...]]]
                     [--regexp REGEXP] [--region REGION]
                     [--coordinate_separator COORDINATE_SEPARATOR]
                     [--pair_separator PAIR_SEPARATOR] [--min_iou MIN_IOU]
                     [--invert_regions]

Only forwards images that have the specified label(s) present.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --labels [LABELS [LABELS ...]]
                        The labels to use (default: None)
  --regexp REGEXP       Regular expression for using only a subset of labels
                        (default: None)
  --region REGION       List of x/y pairs defining the region that the object
                        must overlap with in order to be included. Values
                        between 0-1 are considered normalized, otherwise
                        absolute pixels. (default: None)
  --coordinate_separator COORDINATE_SEPARATOR
                        the separator between coordinates (default: ;)
  --pair_separator PAIR_SEPARATOR
                        the separator between the x and y of a pair (default:
                        ,)
  --min_iou MIN_IOU     The minimum IoU (intersect over union) that the object
                        must have with the region in order to be considered an
                        overlap (object detection only) (default: None)
  --invert_regions      Inverts the matching sense from 'labels have to
                        overlap at least one of the region(s)' to 'labels
                        cannot overlap any region' (default: False)
```
