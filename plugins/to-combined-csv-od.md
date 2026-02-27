# to-combined-csv-od

* accepts: idc.api.ObjectDetectionData

Saves all the object detection information in a single CSV file.

```
usage: to-combined-csv-od [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [--skip] -o OUTPUT [-p] [-m]

Saves all the object detection information in a single CSV file.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -o OUTPUT, --output OUTPUT
                        The CSV file to store the object detection information
                        in. Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  -p, --output_polygon  Whether to output any polygon information as well
                        (default: False)
  -m, --output_meta     Whether to output any meta-data information as well
                        (default: False)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
