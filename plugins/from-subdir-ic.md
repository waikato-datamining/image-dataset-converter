# from-subdir-ic

* generates: idc.base.imgcls.ImageClassificationData

Loads images from sub-directories, uses the name of the sub-directory as classification label.

```
usage: from-subdir-ic [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]

Loads images from sub-directories, uses the name of the sub-directory as
classification label.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the directory with the sub-directories
                        containing the images (default: None)
```