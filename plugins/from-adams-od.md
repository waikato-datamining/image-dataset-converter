# from-adams-od

* generates: idc.api.ObjectDetectionData

Loads the bounding box and/or polygon definitions from the associated .report file.

```
usage: from-adams-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                     [--resume_from RESUME_FROM] [-p PREFIX]

Loads the bounding box and/or polygon definitions from the associated .report
file.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the report file(s) to read; glob syntax is
                        supported; Supported placeholders: {HOME}, {CWD},
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the report files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.report' (default: None)
  -p PREFIX, --prefix PREFIX
                        The field prefix in the .report files that identifies
                        bbox/polygon object definitions (default: Object.)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
