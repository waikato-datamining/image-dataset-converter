# sort-pixels

* accepts: idc.api.ImageData
* generates: seppl.AnyData

Sorts the (grayscale) pixels in ascending order per row.

```
usage: sort-pixels [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip]
                   [-s {cols,rows,cols-then-rows,rows-then-cols}]

Sorts the (grayscale) pixels in ascending order per row.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s {cols,rows,cols-then-rows,rows-then-cols}, --sorting {cols,rows,cols-then-rows,rows-then-cols}
                        How to sort the pixels. (default: cols)
```
