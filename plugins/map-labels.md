# map-labels

* accepts: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData

Maps labels from one set to another.

```
usage: map-labels [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [-m [old=new [old=new ...]]]

Maps labels from one set to another.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -m [old=new [old=new ...]], --mapping [old=new [old=new ...]]
                        The labels to use (default: None)
```
