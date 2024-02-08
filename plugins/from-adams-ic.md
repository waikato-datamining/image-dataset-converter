# from-adams-ic

* generates: idc.base.ImageClassificationData

Loads the image classification from the specified class field in the associated .report file.

```
usage: from-adams-ic [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                     [-I [INPUT_LIST [INPUT_LIST ...]]] -c FIELD

Loads the image classification from the specified class field in the
associated .report file.

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
                        Path to the text file(s) listing the data files to use
                        (default: None)
  -c FIELD, --class_field FIELD
                        The report field containing the image classification
                        label (default: None)
```
