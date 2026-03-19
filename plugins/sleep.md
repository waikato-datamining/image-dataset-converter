# sleep

* accepts: seppl.AnyData
* generates: seppl.AnyData

Waits the specified number of seconds before forwarding the data. A time of 0 means no waiting.

```
usage: sleep [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
             [--skip] [-w SEC]

Waits the specified number of seconds before forwarding the data. A time of 0
means no waiting.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -w SEC, --wait_time SEC
                        The time in seconds to wait. (default: 0.0)
```
