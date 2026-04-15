# df-image-data

Expands the placeholders in the format string using the available image data.

```
usage: df-image-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [-f OUTPUT_FORMAT]

Expands the placeholders in the format string using the available image data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -f OUTPUT_FORMAT, --output_format OUTPUT_FORMAT
                        The format to use for the output, available
                        placeholders: data, image-name, image-format, image-
                        width, image-height, has-annotations, annotations
                        (default: data)
```
