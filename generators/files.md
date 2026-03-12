# files

Iterates over files that it finds. Can be limited to files that match a regular expression. Available variables: absfile|relfile|filename|filename_noext. absfile: the absolute file, relfile: the relative file to the search path, filename: the file name (no parent path), filename_noext: the file name without extension (no parent path).

```
usage: files [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME] -p
             DIR [DIR ...] [-r] [--regexp REGEXP] [-s]

Iterates over files that it finds. Can be limited to files that match a
regular expression. Available variables:
absfile|relfile|filename|filename_noext. absfile: the absolute file, relfile:
the relative file to the search path, filename: the file name (no parent
path), filename_noext: the file name without extension (no parent path).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -p DIR [DIR ...], --path DIR [DIR ...]
                        The directory/directories to search (default: None)
  -r, --recursive       Whether to search for files recursively. (default:
                        False)
  --regexp REGEXP       The regular expression to use for matching files;
                        matches all if not provided. (default: None)
  -s, --sort            Whether to sort the list of directories. (default:
                        False)
```
