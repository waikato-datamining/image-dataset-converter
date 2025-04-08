# to-pyfunc

* accepts: idc.api.ImageData

Processes the images of the specified data type via the declared Python function. The function must take an image container as input (matching the data type class) and an optional 'split' string parameter.

```
usage: to-pyfunc [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--skip]
                 [--split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]]
                 [--split_names SPLIT_NAMES [SPLIT_NAMES ...]]
                 [--split_group SPLIT_GROUP] -f FUNCTION -t {ic,is,od}

Processes the images of the specified data type via the declared Python
function. The function must take an image container as input (matching the
data type class) and an optional 'split' string parameter.

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
  -f FUNCTION, --function FUNCTION
                        The Python function to use, format:
                        module_name:function_name (default: None)
  -t {ic,is,od}, --data_type {ic,is,od}
                        The type of data to forward (default: None)
```
