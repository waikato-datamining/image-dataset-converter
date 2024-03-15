# convert-image-format

* accepts: seppl.AnyData
* generates: seppl.AnyData

Converts the image format to the specified type.

```
usage: convert-image-format [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                            [-N LOGGER_NAME] -f {JPEG,PNG,BMP}

Converts the image format to the specified type.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -f {JPEG,PNG,BMP}, --image_format {JPEG,PNG,BMP}
                        The image format to use (default: None)
```
