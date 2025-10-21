# annotations-to-storage

* accepts: seppl.AnyData
* generates: seppl.AnyData

Places the annotations in storage under the specified name.

```
usage: annotations-to-storage [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                              [-N LOGGER_NAME] [--skip] -s STORAGE_NAME

Places the annotations in storage under the specified name.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s STORAGE_NAME, --storage_name STORAGE_NAME
                        The name to store the annotations under in internal
                        storage. (default: None)
```
