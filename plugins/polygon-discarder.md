# polygon-discarder

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Removes polygons that fall outside the specified point limits (skips annotations with no polygons).

```
usage: polygon-discarder [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [-N LOGGER_NAME] [-m MIN_POINTS] [-M MAX_POINTS]

Removes polygons that fall outside the specified point limits (skips
annotations with no polygons).

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -m MIN_POINTS, --min_points MIN_POINTS
                        The minimum number of points (default: None)
  -M MAX_POINTS, --max_points MAX_POINTS
                        The maximum number of points (default: None)
```
