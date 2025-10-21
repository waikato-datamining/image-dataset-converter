# list-files

* generates: str

Lists files in the specified directory and forwards them.

```
usage: list-files [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] -i DIR [-r REGEXP] [--as_list]

Lists files in the specified directory and forwards them.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i DIR, --input_dir DIR
                        The directory to list the files in; Supported
                        placeholders: {HOME}, {CWD}, {TMP} (default: None)
  -r REGEXP, --regexp REGEXP
                        The regular expression that the files must match.
                        (default: .*)
  --as_list             Whether to forward the files as a list or one by one.
                        (default: False)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
