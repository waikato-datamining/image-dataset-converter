# to-yolo-od

* accepts: idc.api.ObjectDetectionData

Saves the bounding box/polygon definitions in YOLO .txt format. By default, places images in the 'images' subdir and the annotations in 'labels'.

```
usage: to-yolo-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                  [-n SPLIT_NAMES [SPLIT_NAMES ...]] -o OUTPUT
                  [--image_subdir DIR] [--labels_subdir DIR] [-p]
                  [--categories [CATEGORIES ...]] [--labels LABELS]
                  [--labels_csv LABELS_CSV] [--annotations_only]

Saves the bounding box/polygon definitions in YOLO .txt format. By default,
places images in the 'images' subdir and the annotations in 'labels'.

options:
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
                        The directory to store the images/.txt files in. Any
                        defined splits get added beneath there. (default:
                        None)
  --image_subdir DIR    The name of the sub-dir to use for storing the images
                        in. (default: None)
  --labels_subdir DIR   The name of the sub-dir to use for storing the
                        annotations in. (default: None)
  -p, --use_polygon_format
                        Whether to write the annotations in polygon format
                        rather than bbox format (default: False)
  --categories [CATEGORIES ...]
                        The predefined order of categories. (default: None)
  --labels LABELS       The text file (no path) with the comma-separated list
                        of labels (default: None)
  --labels_csv LABELS_CSV
                        The CSV file (no path) to write the label mapping to
                        (index and label) (default: None)
  --annotations_only    Outputs only the annotations and skips the base image.
                        (default: False)
```
