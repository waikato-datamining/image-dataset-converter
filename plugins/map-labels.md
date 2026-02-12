# map-labels

* accepts: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData
* generates: idc.api.ObjectDetectionData, idc.api.ImageClassificationData, idc.api.ImageSegmentationData

Maps labels from one set to another.

```
usage: map-labels [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [--skip] [-m [old=new ...]]
                  [-o [LABEL ...]] [-O [REGEXP ...]] [-n LABEL]

Maps labels from one set to another.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m [old=new ...], --mapping [old=new ...]
                        The labels to use (default: None)
  -o [LABEL ...], --old_labels [LABEL ...]
                        The old labels to replace with the new one, requires
                        -n/--new_label (default: None)
  -O [REGEXP ...], --old_regexps [REGEXP ...]
                        The regexps for matching the old labels to replace
                        with the new one, requires -n/--new_label (default:
                        None)
  -n LABEL, --new_label LABEL
                        The new label to use (default: None)
```
