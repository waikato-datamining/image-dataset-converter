# polygon-simplifier

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Simplifies polygons according to the tolerance parameter: the smaller the tolerance, the closer to the original.

```
usage: polygon-simplifier [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [-t TOLERANCE]

Simplifies polygons according to the tolerance parameter: the smaller the
tolerance, the closer to the original.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -t TOLERANCE, --tolerance TOLERANCE
                        The tolerance for the simplification. (default: 0.01)
```
