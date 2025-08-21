# text-file

Outputs the lines from the text file (non-empty and not starting with #).

```
usage: text-file [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-n NAME] -f FILE

Outputs the lines from the text file (non-empty and not starting with #).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -n NAME, --var_name NAME
                        The name of the variable (default: v)
  -f FILE, --text_file FILE
                        The text file with the values to use. (default: None)
```
