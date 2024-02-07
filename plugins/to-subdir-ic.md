# to-subdir-ic

* accepts: idc.base.imgcls.ImageClassificationData

Saves images to sub-directories, using the classification label for the sub-directory.

```
usage: to-subdir-ic [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] -o OUTPUT

Saves images to sub-directories, using the classification label for the sub-
directory.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -o OUTPUT, --output OUTPUT
                        The directory to create the sub-directories in
                        according to the image labels. (default: None)
```
