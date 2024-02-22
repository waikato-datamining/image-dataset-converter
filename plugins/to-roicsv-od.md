# to-roicsv-od

* accepts: idc.api.ObjectDetectionData

Saves the bounding box/polygon definitions in a ROI .csv file alongside the image.

```
usage: to-roicsv-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                    [-n SPLIT_NAMES [SPLIT_NAMES ...]] -o OUTPUT [-s SUFFIX]

Saves the bounding box/polygon definitions in a ROI .csv file alongside the
image.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -r SPLIT_RATIOS [SPLIT_RATIOS ...], --split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (must sum up to 100) (default: None)
  -n SPLIT_NAMES [SPLIT_NAMES ...], --split_names SPLIT_NAMES [SPLIT_NAMES ...]
                        The split names to use for the generated splits.
                        (default: None)
  -o OUTPUT, --output OUTPUT
                        The directory to store the images/.report files in.
                        Any defined splits get added beneath there. (default:
                        None)
  -s SUFFIX, --suffix SUFFIX
                        The suffix used by the ROI CSV files. (default:
                        -rois.csv)
```