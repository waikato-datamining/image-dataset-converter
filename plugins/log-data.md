# log-data

* accepts: seppl.AnyData
* generates: seppl.AnyData

Logs information about the data passing through, either storing it in the specified file or outputting it on stdout.

```
usage: log-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--skip] -f FORMAT [-o FILE] [-d]

Logs information about the data passing through, either storing it in the
specified file or outputting it on stdout.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f FORMAT, --log_format FORMAT
                        The format to use for logging; {NAME}: for
                        NameSupporter data, {SOURCE}: for SourceSupporter
                        data, {HAS_ANNOTATION}/{ANNOTATION}: for
                        AnnotationHandler data, {META.<key>}: for
                        MetaDataHandler data (<key> is the key in the meta-
                        data); use \t for tab and \n for new-line (default:
                        None)
  -o FILE, --output_file FILE
                        The file to write the logging data to; Supported
                        placeholders: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  -d, --delete_on_initialize
                        Whether to remove any existing file when initializing
                        the writer. (default: False)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
* `{INPUT_PATH}`: The directory part of the current input, i.e., `/some/where` of input `/some/where/file.txt`.
* `{INPUT_NAMEEXT}`: The name (incl extension) of the current input, i.e., `file.txt` of input `/some/where/file.txt`.
* `{INPUT_NAMENOEXT}`: The name (excl extension) of the current input, i.e., `file` of input `/some/where/file.txt`.
* `{INPUT_EXT}`: The extension of the current input (incl dot), i.e., `.txt` of input `/some/where/file.txt`.
* `{INPUT_PARENT_PATH}`: The directory part of the parent directory of the current input, i.e., `/some` of input `/some/where/file.txt`.
* `{INPUT_PARENT_NAME}`: The name of the parent directory of the current input, i.e., `where` of input `/some/where/file.txt`.
