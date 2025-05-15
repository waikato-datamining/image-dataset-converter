# depth-to-greyscale

* accepts: idc.api.DepthData
* generates: idc.api.DepthData
* alias(es): depth-to-greyscale

Turns the depth information into a grayscale image.

```
usage: depth-to-grayscale [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [--skip] [-m MIN_VALUE]
                          [-M MAX_VALUE] -t {dp,ic,is,od}

Turns the depth information into a grayscale image.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m MIN_VALUE, --min_value MIN_VALUE
                        The minimum value to use, smaller values get set to
                        this. (default: None)
  -M MAX_VALUE, --max_value MAX_VALUE
                        The maximum value to use, larger values get set to
                        this. (default: None)
  -t {dp,ic,is,od}, --data_type {dp,ic,is,od}
                        The type of data to forward (default: None)
```
