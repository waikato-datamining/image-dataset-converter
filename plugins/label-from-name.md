# label-from-name

* accepts: idc.api.ImageClassificationData
* generates: idc.api.ImageClassificationData

Extracts the classification label from the image name.

```
usage: label-from-name [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [-r REGEXP]

Extracts the classification label from the image name.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -r REGEXP, --regexp REGEXP
                        The regular expression apply to the image name, with
                        the 1st group being used as the label. (default: None)
```
