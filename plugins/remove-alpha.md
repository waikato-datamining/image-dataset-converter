# remove-alpha

* accepts: idc.api.ImageData
* generates: idc.api.ImageData

Removes the alpha channel in the base image.

```
usage: remove-alpha [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip]

Removes the alpha channel in the base image.

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
