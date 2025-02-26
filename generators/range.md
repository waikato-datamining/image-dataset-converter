# range

Iterates over a range of values.

```
usage: range [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
             [-n NAME] -f START -t END [-s STEP]

Iterates over a range of values.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -n NAME, --var_name NAME
                        The name of the variable (default: i)
  -f START, --from START
                        The starting value (default: None)
  -t END, --to END      The end value (excluded) (default: None)
  -s STEP, --step STEP  The increment between values (default: 1)
```
