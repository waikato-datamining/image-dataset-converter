# from-blue-channel-is

* generates: idc.api.ImageSegmentationData

Loads the annotations from associated blue channel JPG/PNG files.

```
usage: from-blue-channel-is [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                            [-N LOGGER_NAME] [-i [INPUT ...]]
                            [-I [INPUT_LIST ...]] [--resume_from RESUME_FROM]
                            [--image_path_rel PATH]
                            [--labels LABEL [LABEL ...]]
                            [--background BACKGROUND]

Loads the annotations from associated blue channel JPG/PNG files.

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
                        Path to the text file(s) listing the text PNG to use;
                        Supported placeholders: {HOME}, {CWD}, {TMP} (default:
                        None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.png' (default: None)
  --image_path_rel PATH
                        The relative path from the annotations to the images
                        directory (default: None)
  --labels LABEL [LABEL ...]
                        The labels that the indices represent. (default: None)
  --background BACKGROUND
                        The index (0-255) that is used for the background
                        (default: 0)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
