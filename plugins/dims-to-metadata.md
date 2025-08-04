# dims-to-metadata

* accepts: seppl.AnyData
* generates: seppl.AnyData

Transfers the image dimensions to the meta-data.

```
usage: dims-to-metadata [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [-N LOGGER_NAME] [--skip] [--width_field FIELD]
                        [--height_field FIELD]

Transfers the image dimensions to the meta-data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --width_field FIELD   The metadata field for the width (default: width)
  --height_field FIELD  The metadata field for the height (default: height)
```
