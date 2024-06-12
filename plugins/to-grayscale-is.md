# to-grayscale-is

* accepts: idc.api.ImageSegmentationData

Saves the annotations as grayscale PNG files. The associated JPG images can be placed in folder relative to the annotation.

```
usage: to-grayscale-is [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                       [-n SPLIT_NAMES [SPLIT_NAMES ...]] -o OUTPUT
                       [--image_path_rel PATH] [--annotations_only]

Saves the annotations as grayscale PNG files. The associated JPG images can be
placed in folder relative to the annotation.

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
                        The directory to store the images files in. Any
                        defined splits get added beneath there. (default:
                        None)
  --image_path_rel PATH
                        The relative path from the annotations to the images
                        directory (default: None)
  --annotations_only    Outputs only the annotations and skips the base image.
                        (default: False)
```
