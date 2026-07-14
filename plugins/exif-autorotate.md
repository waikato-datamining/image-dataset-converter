# exif-autorotate

* accepts: seppl.AnyData
* generates: seppl.AnyData

Automatically rotates the image according to the EXIF information (if applicable). May not work as expected if auto-rotation is enforced via environment variable IDC_EXIF_AUTOROTATE as the implicit rotation will lose the EXIF information.

```
usage: exif-autorotate [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip]

Automatically rotates the image according to the EXIF information (if
applicable). May not work as expected if auto-rotation is enforced via
environment variable IDC_EXIF_AUTOROTATE as the implicit rotation will lose
the EXIF information.

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
