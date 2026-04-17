# sanitize-name

* accepts: seppl.AnyData
* generates: seppl.AnyData

Removes unwanted characters from file names.

```
usage: sanitize-name [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [--skip] [-a ALLOWED] [-r REPLACE]

Removes unwanted characters from file names.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -a ALLOWED, --allowed ALLOWED
                        The characters that are allowed in names. (default: ab
                        cdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123
                        456789_-.)
  -r REPLACE, --replace REPLACE
                        The string to replace the unwanted characters with,
                        leave empty to complete replace them. (default: )
```
