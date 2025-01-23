# od-to-is

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ImageSegmentationData

Converts object detection annotations into image segmentation ones.

```
usage: od-to-is [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--labels [LABELS ...]] [--regexp REGEXP]

Converts object detection annotations into image segmentation ones.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --labels [LABELS ...]
                        The labels to use (default: None)
  --regexp REGEXP       Regular expression for using only a subset of labels
                        (default: None)
```
