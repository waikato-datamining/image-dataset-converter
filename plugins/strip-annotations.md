# strip-annotations

* accepts: seppl.AnyData
* generates: seppl.AnyData

Removes all annotations from the data coming through.

```
usage: strip-annotations [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [-N LOGGER_NAME]

Removes all annotations from the data coming through.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
```
