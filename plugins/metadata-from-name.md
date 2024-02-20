# metadata-from-name

* accepts: idc.api.ImageData
* generates: idc.api.ImageClassificationData, idc.api.ImageSegmentationData, idc.api.ObjectDetectionData

Extracts a sub-string from the image name and stores them in the meta-data.

```
usage: metadata-from-name [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [-r REGEXP] [-k METADATA_KEY]

Extracts a sub-string from the image name and stores them in the meta-data.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -r REGEXP, --regexp REGEXP
                        The regular expression apply to the image name, with
                        the 1st group being used as the meta-data value.
                        (default: None)
  -k METADATA_KEY, --metadata_key METADATA_KEY
                        The key in the meta-data to store the extracted sub-
                        string under. (default: None)
```
