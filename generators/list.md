# list

Outputs the specified values.

```
usage: list [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
            [-n NAME] [-v VALUE [VALUE ...]]

Outputs the specified values.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -n NAME, --var_name NAME
                        The name of the variable (default: v)
  -v VALUE [VALUE ...], --values VALUE [VALUE ...]
                        The list of values to use. (default: None)
```
