# find-contours

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Finds the contours in the binary image and stores them as polygons in the annotations.

```
usage: find-contours [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [--skip] [--label LABEL] [-m MIN_SIZE]
                     [-M MAX_SIZE]

Finds the contours in the binary image and stores them as polygons in the
annotations.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --label LABEL         The label to use for the detected contours. (default:
                        None)
  -m MIN_SIZE, --min_size MIN_SIZE
                        The minimum width or height that detected contours
                        must have. (default: None)
  -M MAX_SIZE, --max_size MAX_SIZE
                        The maximum width or height that detected contours can
                        have. (default: None)
```
