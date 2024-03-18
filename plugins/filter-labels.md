# filter-labels

* accepts: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData

Filters out labels according to the parameters.

```
usage: filter-labels [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [--labels [LABELS [LABELS ...]]]
                     [--regexp REGEXP] [--region x,y,w,h] [--min_iou MIN_IOU]

Filters out labels according to the parameters.

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
  --region x,y,w,h      Region that the object must overlap with in order to
                        be included (object detection only). Between 0-1 the
                        values are considered normalized, otherwise absolute
                        pixels. (default: None)
  --min_iou MIN_IOU     The minimum IoU (intersect over union) that the object
                        must have with the region in order to be considered an
                        overlap (object detection only) (default: None)
```
