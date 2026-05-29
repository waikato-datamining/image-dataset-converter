# discard-blurry

* accepts: idc.api.ImageData
* generates: idc.api.ImageData

Discards blurry images, i.e., ones with a laplacian variance that falls below the specified threshold.

```
usage: discard-blurry [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [--skip] [-t NUM]

Discards blurry images, i.e., ones with a laplacian variance that falls below
the specified threshold.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -t NUM, --threshold NUM
                        The threshold for the laplacian variance. (default:
                        100)
```
