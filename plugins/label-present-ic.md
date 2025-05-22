# label-present-ic

* accepts: idc.api.ImageClassificationData
* generates: idc.api.ImageClassificationData

Only forwards images that have the specified label(s) present.

```
usage: label-present-ic [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [-N LOGGER_NAME] [--skip] [--labels [LABELS ...]]

Only forwards images that have the specified label(s) present.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --labels [LABELS ...]
                        The labels to use (default: None)
```
