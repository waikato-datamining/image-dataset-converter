# console

* accepts: seppl.AnyData

Prints the data to stdout using the supplied data formatter.

```
usage: console [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
               [--skip] [-f DATA_FORMATTER]

Prints the data to stdout using the supplied data formatter.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f DATA_FORMATTER, --data_formatter DATA_FORMATTER
                        The data formatter to apply (default: df-simple-
                        string)
```
