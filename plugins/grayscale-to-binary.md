# greyscale-to-binary

* accepts: idc.api.ImageData
* generates: seppl.AnyData
* alias(es): greyscale-to-binary

Turns grayscale images into binary ones. A grayscale image is required. You can use the 'rgb-to-grayscale' for the conversion.

```
usage: grayscale-to-binary [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                           [-N LOGGER_NAME] [--skip] [-t THRESHOLD]

Turns grayscale images into binary ones. A grayscale image is required. You
can use the 'rgb-to-grayscale' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -t THRESHOLD, --threshold THRESHOLD
                        The threshold to use (0-255). (default: 127)
```
