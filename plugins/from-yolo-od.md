# from-yolo-od

* generates: idc.api.ObjectDetectionData

Loads the bounding box and/or polygon definitions from the associated .txt file in YOLO format.

```
usage: from-yolo-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                    [--image_path_rel PATH] [-p] [--labels FILE]

Loads the bounding box and/or polygon definitions from the associated .txt
file in YOLO format.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the text file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the text files to use
                        (default: None)
  --image_path_rel PATH
                        The relative path from the annotations to the images
                        directory (default: None)
  -p, --use_polygon_format
                        Whether to read the annotations in polygon format
                        rather than bbox format (default: False)
  --labels FILE         The text file with the comma-separated list of labels
                        (default: None)
```
