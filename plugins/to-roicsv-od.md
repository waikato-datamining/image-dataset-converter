# to-roicsv-od

* accepts: idc.api.ObjectDetectionData

Saves the bounding box/polygon definitions in a ROI .csv file alongside the image.

```
usage: to-roicsv-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip]
                    [--split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]]
                    [--split_names SPLIT_NAMES [SPLIT_NAMES ...]]
                    [--split_group SPLIT_GROUP] -o OUTPUT [-s SUFFIX]
                    [--size_mode] [--annotations_only]

Saves the bounding box/polygon definitions in a ROI .csv file alongside the
image.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (must sum up to 100) (default: None)
  --split_names SPLIT_NAMES [SPLIT_NAMES ...]
                        The split names to use for the generated splits.
                        (default: None)
  --split_group SPLIT_GROUP
                        The regular expression with a single group used for
                        keeping items in the same split, e.g., for identifying
                        the base name of a file or the sample ID. (default:
                        None)
  -o OUTPUT, --output OUTPUT
                        The directory to store the images/.csv files in. Any
                        defined splits get added beneath there. Supported
                        placeholders: {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -s SUFFIX, --suffix SUFFIX
                        The suffix used by the ROI CSV files. (default:
                        -rois.csv)
  --size_mode           Whether to output w/h rather than x1/y1. (default:
                        False)
  --annotations_only    Outputs only the annotations and skips the base image.
                        (default: False)
```

Available placeholders:

* `{INPUT_PATH}`: The directory part of the current input, i.e., `/some/where` of input `/some/where/file.txt`.
* `{INPUT_NAMEEXT}`: The name (incl extension) of the current input, i.e., `file.txt` of input `/some/where/file.txt`.
* `{INPUT_NAMENOEXT}`: The name (excl extension) of the current input, i.e., `file` of input `/some/where/file.txt`.
* `{INPUT_EXT}`: The extension of the current input (incl dot), i.e., `.txt` of input `/some/where/file.txt`.
* `{INPUT_PARENT_PATH}`: The directory part of the parent directory of the current input, i.e., `/some` of input `/some/where/file.txt`.
* `{INPUT_PARENT_NAME}`: The name of the parent directory of the current input, i.e., `where` of input `/some/where/file.txt`.
