# rename

* accepts: idc.api.ImageData
* generates: seppl.AnyData

Renames files using a user-supplied format.

```
usage: rename [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [-f NAME_FORMAT]

Renames files using a user-supplied format.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -f NAME_FORMAT, --name-format NAME_FORMAT
                        The format for the new name. Available placeholders: -
                        {name}: the name of the file, without path or
                        extension. - {ext}: the extension of the file (incl
                        dot). - {occurrences}: the number of times this name
                        (excl extension) has been encountered. - {count}: the
                        number of files encountered so far. - {[p]+dir}: the
                        parent directory of the file: 'p': immediate parent,
                        the more the p's the higher up in the hierarchy.
                        (default: {name}{ext})
```
