# from-multi

* generates: idc.api.ImageData

Reads data using the specified base readers and combines their output.

```
usage: from-multi [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] -r READER [READER ...]
                  [-o {sequential,interleaved}] -t {dp,ic,is,od}

Reads data using the specified base readers and combines their output.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -r READER [READER ...], --reader READER [READER ...]
                        The command-line defining the base reader. (default:
                        None)
  -o {sequential,interleaved}, --read_order {sequential,interleaved}
                        How to use the output from the readers. (default:
                        sequential)
  -t {dp,ic,is,od}, --data_type {dp,ic,is,od}
                        The type of data to forward (default: None)
```

The following data types are available:

* dp: depth
* ic: image classification
* is: image segmentation
* od: object detection

