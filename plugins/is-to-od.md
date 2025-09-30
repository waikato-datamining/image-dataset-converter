# is-to-od

* accepts: idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData

Converts image segmentation annotations into object detection ones by finding contours in the layers that match the specified labels/regexp. Using the min/max parameters, contours can be filtered out that are too small or too large.

```
usage: is-to-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--skip] [--labels [LABELS ...]] [--regexp REGEXP]
                [-m MIN_SIZE] [-M MAX_SIZE]

Converts image segmentation annotations into object detection ones by finding
contours in the layers that match the specified labels/regexp. Using the
min/max parameters, contours can be filtered out that are too small or too
large.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --labels [LABELS ...]
                        The labels to use (default: None)
  --regexp REGEXP       Regular expression for using only a subset of labels
                        (default: None)
  -m MIN_SIZE, --min_size MIN_SIZE
                        The minimum width or height that detected contours
                        must have. (default: None)
  -M MAX_SIZE, --max_size MAX_SIZE
                        The maximum width or height that detected contours can
                        have. (default: None)
```
