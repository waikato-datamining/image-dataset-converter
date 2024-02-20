# from-data

* generates: idc.api.ImageData

Loads the images and forwards them as the specified data type.

```
usage: from-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                 [-I [INPUT_LIST [INPUT_LIST ...]]] -t {ic,is,od}

Loads the images and forwards them as the specified data type.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the image file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST [INPUT_LIST ...]], --input_list [INPUT_LIST [INPUT_LIST ...]]
                        Path to the text file(s) listing the image files to
                        use (default: None)
  -t {ic,is,od}, --data_type {ic,is,od}
                        The type of data to forward (default: None)
```
