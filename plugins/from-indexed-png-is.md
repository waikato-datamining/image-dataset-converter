# from-indexed-png-is

* generates: idc.api.ImageSegmentationData

Loads the annotations from associated indexed PNG files.

```
usage: from-indexed-png-is [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                           [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                           [-I [INPUT_LIST [INPUT_LIST ...]]]
                           [--image_path_rel PATH]
                           [--labels LABEL [LABEL ...]]

Loads the annotations from associated indexed PNG files.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the report file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST [INPUT_LIST ...]], --input_list [INPUT_LIST [INPUT_LIST ...]]
                        Path to the text file(s) listing the text files to use
                        (default: None)
  --image_path_rel PATH
                        The relative path from the annotations to the images
                        directory (default: None)
  --labels LABEL [LABEL ...]
                        The labels that the indices represent. (default: None)
```
