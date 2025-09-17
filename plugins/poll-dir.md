# poll-dir

* generates: seppl.AnyData

Polls a directory for files and presents them to the base reader.

```
usage: poll-dir [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                -b BASE_READER -i DIR_IN [-o DIR_OUT] [-w POLL_WAIT]
                [-W PROCESS_WAIT] [-a {nothing,move,delete}] -e EXTENSIONS
                [EXTENSIONS ...] [-O [OTHER_INPUT_FILES ...]] [-m MAX_FILES]

Polls a directory for files and presents them to the base reader.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -b BASE_READER, --base_reader BASE_READER
                        The command-line of the reader for reading the files
                        (default: None)
  -i DIR_IN, --dir_in DIR_IN
                        The directory to poll; Supported placeholders: {HOME},
                        {CWD}, {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -o DIR_OUT, --dir_out DIR_OUT
                        The directory to move the files to; Supported
                        placeholders: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  -w POLL_WAIT, --poll_wait POLL_WAIT
                        The poll interval in seconds (default: 1.0)
  -W PROCESS_WAIT, --process_wait PROCESS_WAIT
                        The number of seconds to wait before processing the
                        polled files (e.g., waiting for files to be fully
                        written) (default: 0.0)
  -a {nothing,move,delete}, --action {nothing,move,delete}
                        The action to apply to the input files; 'move' moves
                        the files to --dir_out directory (default: move)
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        The extensions of the files to poll (incl. dot)
                        (default: None)
  -O [OTHER_INPUT_FILES ...], --other_input_files [OTHER_INPUT_FILES ...]
                        The glob expression(s) for capturing other files apart
                        from the input files; use {NAME} in the glob
                        expression for the current name (default: None)
  -m MAX_FILES, --max_files MAX_FILES
                        The maximum number of files in a single poll; <1 for
                        unlimited (default: -1)
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
