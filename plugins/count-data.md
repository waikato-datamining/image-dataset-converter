# count-data

* accepts: seppl.AnyData
* generates: seppl.AnyData

Counts the items of data passing through and outputs the total at the end.

```
usage: count-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [--skip] [-p STR]

Counts the items of data passing through and outputs the total at the end.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -p STR, --prefix STR  The prefix string to use for the output of the total
                        count. (default: total count: )
```
