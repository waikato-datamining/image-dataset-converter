# coerce-mask

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Coerces the bounds of the annotations to all be polygon-masks. Annotations which already have polygons keep theirs, but those without are given a rectangular polygon in the shape of their bounding box.

```
usage: coerce-mask [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip]

Coerces the bounds of the annotations to all be polygon-masks. Annotations
which already have polygons keep theirs, but those without are given a
rectangular polygon in the shape of their bounding box.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
```
