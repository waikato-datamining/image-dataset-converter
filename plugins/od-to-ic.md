# od-to-ic

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ImageClassificationData

Converts object detection annotations into image classification ones.

```
usage: od-to-ic [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--skip] [-m {error,majority,single,skip}]

Converts object detection annotations into image classification ones.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m {error,majority,single,skip}, --multiplicity {error,majority,single,skip}
                        How to handle instances with more than one located
                        object (default: error)
```
