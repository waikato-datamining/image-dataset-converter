# discard-by-name

* accepts: seppl.AnyData
* generates: seppl.AnyData

Discards files based on list of names, list of paths and/or regular expressions that names must match.

```
usage: discard-by-name [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] [-i [NAMES ...]]
                       [-I NAMES_FILE] [-p [PATHS ...]] [-r [REGEXPS ...]]
                       [-R REGEXPS_FILE] [-e] [-V]

Discards files based on list of names, list of paths and/or regular
expressions that names must match.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -i [NAMES ...], --names [NAMES ...]
                        The name(s) to drop. (default: None)
  -I NAMES_FILE, --names_file NAMES_FILE
                        The text file with the name(s) to drop. (default:
                        None)
  -p [PATHS ...], --paths [PATHS ...]
                        The directories with files to ignore. (default: None)
  -r [REGEXPS ...], --regexps [REGEXPS ...]
                        The regular expressions for matching name(s) to drop.
                        (default: None)
  -R REGEXPS_FILE, --regexps_file REGEXPS_FILE
                        The text file with regular expressions for matching
                        name(s) to drop. (default: None)
  -e, --remove_ext      Whether to remove the extension (and dot) before
                        matching. (default: False)
  -V, --invert          Whether to invert the matching sense. (default: False)
```
