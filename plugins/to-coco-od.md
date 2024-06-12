# to-coco-od

* accepts: idc.api.ObjectDetectionData

Saves the bounding box/polygon definitions in MS COCO .json format.

```
usage: to-coco-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                  [-n SPLIT_NAMES [SPLIT_NAMES ...]] -o OUTPUT
                  [--license_name LICENSE_NAME] [--license_url LICENSE_URL]
                  [--categories [CATEGORIES [CATEGORIES ...]]]
                  [--error_on_new_category]
                  [--default_supercategory DEFAULT_SUPERCATEGORY]
                  [--sort_categories]
                  [--category_output_file CATEGORY_OUTPUT_FILE]
                  [--annotations_only]

Saves the bounding box/polygon definitions in MS COCO .json format.

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
                        The directory to store the images/.json files in. Any
                        defined splits get added beneath there. (default:
                        None)
  --license_name LICENSE_NAME
                        The name of the license to use. (default: default)
  --license_url LICENSE_URL
                        The URL of the license to use. (default: )
  --categories [CATEGORIES [CATEGORIES ...]]
                        The predefined order of categories. (default: None)
  --error_on_new_category
                        Whether to raise an exception if an unknown category
                        is encountered. (default: False)
  --default_supercategory DEFAULT_SUPERCATEGORY
                        The default super category to use, e.g., 'Object'.
                        (default: Object)
  --sort_categories     Whether to sort the categories. (default: False)
  --category_output_file CATEGORY_OUTPUT_FILE
                        The name of the file (no path) to store the categories
                        in as comma-separated list. (default: None)
  --annotations_only    Outputs only the annotations and skips the base image.
                        (default: False)
```
