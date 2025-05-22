# apply-label-mask

* accepts: idc.api.ImageSegmentationData
* generates: idc.api.ImageSegmentationData

Applies the specified image segmentation label mask to the base image.

```
usage: apply-label-mask [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [-N LOGGER_NAME] [--skip] --label LABEL [--lenient]

Applies the specified image segmentation label mask to the base image.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --label LABEL         The image segmentation label mask to apply to the base
                        image. (default: None)
  --lenient             Missing labels will not generate an error. (default:
                        False)
```
