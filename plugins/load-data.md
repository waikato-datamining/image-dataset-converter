# load-data

* accepts: str
* generates: idc.api.ImageData

Wraps the incoming file name in the specified data type and forwards it. The input file name can contain placeholders.

```
usage: load-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--skip] -t {dp,ic,is,od}

Wraps the incoming file name in the specified data type and forwards it. The
input file name can contain placeholders.

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
```

The following data types are available:

* dp: depth
* ic: image classification
* is: image segmentation
* od: object detection

