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
                        The meta-data field to set (default: None)
  -v VALUE, --value VALUE
                        The value to store in the meta-data; in case of type
                        string, variables in the value get automatically
                        expanded; Supported variables: {HOME}, {CWD}, {TMP},
                        {INPUT_PATH}, {INPUT_NAMEEXT}, {INPUT_NAMENOEXT},
                        {INPUT_EXT}, {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME}
                        (default: None)
  -t {string,bool,numeric}, --as_type {string,bool,numeric}
                        How to interpret the value (default: string)
  -u, --use_current     Whether to use the data passing through instead of the
                        specified value. (default: False)
```

Available variables:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
* `{INPUT_PATH}`: The directory part of the current input, i.e., `/some/where` of input `/some/where/file.txt`.
* `{INPUT_NAMEEXT}`: The name (incl extension) of the current input, i.e., `file.txt` of input `/some/where/file.txt`.
* `{INPUT_NAMENOEXT}`: The name (excl extension) of the current input, i.e., `file` of input `/some/where/file.txt`.
* `{INPUT_EXT}`: The extension of the current input (incl dot), i.e., `.txt` of input `/some/where/file.txt`.
* `{INPUT_PARENT_PATH}`: The directory part of the parent directory of the current input, i.e., `/some` of input `/some/where/file.txt`.
* `{INPUT_PARENT_NAME}`: The name of the parent directory of the current input, i.e., `where` of input `/some/where/file.txt`.
