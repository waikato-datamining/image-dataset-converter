# dirs

Iterates over directories that it finds. Available variables: absdir|reldir|dirname. absdir: the absolute directory, reldir: the relative directory to the search path, dirname: the directory name (no parent path).

```
usage: dirs [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME] -p
            DIR [DIR ...] [-r] [--regexp REGEXP]

Iterates over directories that it finds. Available variables:
absdir|reldir|dirname. absdir: the absolute directory, reldir: the relative
directory to the search path, dirname: the directory name (no parent path).

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -p DIR [DIR ...], --path DIR [DIR ...]
                        The directory/directories to serarch (default: None)
  -r, --recursive       Whether to search for directories recursively.
                        (default: False)
  --regexp REGEXP       The regular expression to use for matching
                        directories; matches all if not provided. (default:
                        None)
```
