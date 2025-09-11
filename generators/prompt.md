# prompt

Prompts the user to enter values for the specified variables.

```
usage: prompt [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [-n NAME [NAME ...]] [-m PROMPT]

Prompts the user to enter values for the specified variables.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -n NAME [NAME ...], --var_names NAME [NAME ...]
                        The list of variable names to prompt the user with.
                        (default: None)
  -m PROMPT, --message PROMPT
                        The custom message to prompt the user with; expects
                        one %s in the template which will get expanded with
                        the variable name. (default: None)
```
