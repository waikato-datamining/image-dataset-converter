# use-mask

* accepts: idc.api.ImageSegmentationData
* generates: idc.api.ImageData

Uses the images segmentation annotations (= mask) as the new base image.

```
usage: use-mask [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--skip] -t {dp,ic,is,od} [-p PALETTE] [--use_rgb]

Uses the images segmentation annotations (= mask) as the new base image.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -t {dp,ic,is,od}, --data_type {dp,ic,is,od}
                        The type of data to forward (default: None)
  -p PALETTE, --palette PALETTE
                        The palette to use; either palette name (auto|colorbli
                        nd12|colorblind15|colorblind24|colorblind8|dark|graysc
                        ale|light|x11) or comma-separated list of R,G,B
                        values. (default: auto)
  --use_rgb             Whether to force RGB mode instead of palette mode.
                        (default: False)
```
