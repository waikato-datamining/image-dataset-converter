# from-storage

* generates: seppl.AnyData

Retrieves the specified object from internal storage.

```
usage: from-storage [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] -s STORAGE_NAME

Retrieves the specified object from internal storage.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -s STORAGE_NAME, --storage_name STORAGE_NAME
                        The name of the object to retrieve from internal
                        storage. (default: None)
```
