# from-roicsv-od

* generates: idc.api.ObjectDetectionData

Loads the bounding box and/or polygon definitions from the associated ROI .csv file.

```
usage: from-roicsv-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                      [-I [INPUT_LIST [INPUT_LIST ...]]] [-s SUFFIX]

Loads the bounding box and/or polygon definitions from the associated ROI .csv
file.

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
                        Path to the text file(s) listing the report files to
                        use (default: None)
  -s SUFFIX, --suffix SUFFIX
                        The suffix used by the ROI CSV files. (default:
                        -rois.csv)
```
