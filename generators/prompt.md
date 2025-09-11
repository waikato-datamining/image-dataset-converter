# prompt

Prompts the user to enter values for the specified variables.

```
usage: prompt [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [-v NAME [NAME ...]]

Prompts the user to enter values for the specified variables.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -v NAME [NAME ...], --var_names NAME [NAME ...]
                        The list of variable names to prompt the user with.
                        (default: None)
```
