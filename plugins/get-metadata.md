# get-metadata

* accepts: seppl.AnyData
* generates: seppl.AnyData

Returns the value of the specified key from the meta-data.

```
usage: get-metadata [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] -f FIELD

Returns the value of the specified key from the meta-data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f FIELD, --field FIELD
                        The meta-data field to set (default: None)
```
