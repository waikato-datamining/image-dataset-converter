# write-labels

* accepts: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData

Collects labels passing through and writes them to the specified file (stdout if not provided).

```
usage: write-labels [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-o OUTPUT_FILE]
                    [-f {text,comma-separated}]

Collects labels passing through and writes them to the specified file (stdout
if not provided).

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        The file to write the labels to; uses stdout if not
                        provided (default: None)
  -f {text,comma-separated}, --output_format {text,comma-separated}
                        The format to use for the labels (default: text)
```
