# set-metadata

* accepts: seppl.AnyData
* generates: seppl.AnyData

Sets the specified key/value pair in the meta-data. Can use the data passing through instead of the specified value as well.

```
usage: set-metadata [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] -f FIELD [-v VALUE]
                    [-t {string,bool,numeric}] [-u]

Sets the specified key/value pair in the meta-data. Can use the data passing
through instead of the specified value as well.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f FIELD, --field FIELD
                        The meta-data field to use in the comparison (default:
                        None)
  -v VALUE, --value VALUE
                        The value to use in the comparison (default: None)
  -t {string,bool,numeric}, --as_type {string,bool,numeric}
                        How to interpret the value (default: string)
  -u, --use_current     Whether to use the data passing through instead of the
                        specified value. (default: False)
```
