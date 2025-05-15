# from-grayscale-dp

* generates: idc.api.DepthData

Loads the depth information from associated grayscale PNG files.

```
usage: from-grayscale-dp [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [-N LOGGER_NAME] [-i [INPUT ...]]
                         [-I [INPUT_LIST ...]] [--resume_from RESUME_FROM]
                         [-m MIN_VALUE] [-M MAX_VALUE] [--image_path_rel PATH]

Loads the depth information from associated grayscale PNG files.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the PNG file(s) to read; glob syntax is
                        supported; Supported placeholders: {HOME}, {CWD},
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the PNG files to use;
                        Supported placeholders: {HOME}, {CWD}, {TMP} (default:
                        None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.png' (default: None)
  -m MIN_VALUE, --min_value MIN_VALUE
                        The minimum value to use, grayscale values get offset
                        by this. (default: None)
  -M MAX_VALUE, --max_value MAX_VALUE
                        The maximum value to use, grayscale values 0-255 get
                        scaled to min/max, requires min to be specified.
                        (default: None)
  --image_path_rel PATH
                        The relative path from the annotations to the images
                        directory (default: None)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
