# dimension-discarder

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Removes annotations which fall outside certain dimensional limits.

```
usage: dimension-discarder [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                           [-N LOGGER_NAME] [--min_width MIN_WIDTH]
                           [--min_height MIN_HEIGHT] [--max_width MAX_WIDTH]
                           [--max_height MAX_HEIGHT] [--min_area MIN_AREA]
                           [--max_area MAX_AREA]

Removes annotations which fall outside certain dimensional limits.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --min_width MIN_WIDTH
                        The minimum width for annotations (default: None)
  --min_height MIN_HEIGHT
                        The minimum height for annotations (default: None)
  --max_width MAX_WIDTH
                        The maximum width for annotations (default: None)
  --max_height MAX_HEIGHT
                        The maximum height for annotations (default: None)
  --min_area MIN_AREA   The minimum area for annotations (polygon if
                        available, otherwise bbox) (default: None)
  --max_area MAX_AREA   The maximum area for annotations (polygon if
                        available, otherwise bbox) (default: None)
```
