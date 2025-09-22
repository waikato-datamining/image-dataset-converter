# count-specks

* accepts: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData
* generates: idc.api.ImageClassificationData, idc.api.ObjectDetectionData, idc.api.ImageSegmentationData

Counts the number of small specks in the image. A binary image is required. You can use the 'grayscale-to-binary' for the conversion.

```
usage: count-specks [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] [-I {skip,fail}]
                    [-a {both,image,annotations}]
                    [-o {as-is,binary,grayscale,rgb}] [-M MAX_AREA] [-i]
                    [-k METADATA_KEY]

Counts the number of small specks in the image. A binary image is required.
You can use the 'grayscale-to-binary' for the conversion.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -I {skip,fail}, --incorrect_format_action {skip,fail}
                        The action to undertake if an invalid input format is
                        encountered. (default: skip)
  -a {both,image,annotations}, --apply_to {both,image,annotations}
                        Where to apply the filter to. (default: image)
  -o {as-is,binary,grayscale,rgb}, --output_format {as-is,binary,grayscale,rgb}
                        The image format to generate as output. (default: as-
                        is)
  -M MAX_AREA, --max_area MAX_AREA
                        The maximum area for the specks in order to count
                        them. (default: 2.0)
  -i, --invert          Whether to invert the binary image, i.e., looking for
                        black specks rather than white ones. (default: False)
  -k METADATA_KEY, --metadata_key METADATA_KEY
                        The key in the meta-data to store the count under.
                        (default: speck-count)
```
