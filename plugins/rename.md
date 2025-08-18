# rename

* accepts: seppl.AnyData
* generates: seppl.AnyData

Renames files using a user-supplied format.

```
usage: rename [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [--skip] [-f NAME_FORMAT]

Renames files using a user-supplied format.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f NAME_FORMAT, --name-format NAME_FORMAT
                        The format for the new name. Available placeholders: -
                        {name}: the name of the file, without path or
                        extension. - {lname}: the lower-case name of the file,
                        without path or extension. - {uname}: the upper-case
                        name of the file, without path or extension. - {ext}:
                        the extension of the file (incl dot). - {lext}: the
                        lower-case extension of the file (incl dot). - {uext}:
                        the upper-case extension of the file (incl dot). -
                        {occurrences}: the number of times this name (excl
                        extension) has been encountered. - {count}: the number
                        of files encountered so far. - {[p]+dir}: the parent
                        directory of the file: 'p': immediate parent, the more
                        the p's the higher up in the hierarchy. (default:
                        {name}{ext})
```
