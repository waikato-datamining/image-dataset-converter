# inspect

* accepts: seppl.AnyData
* generates: seppl.AnyData

Allows inspecting the data flowing through the pipeline.

```
usage: inspect [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
               [--skip] [-m {interactive,non-interactive}]
               [-o {stdout,stderr,logger,file}] [--output_file OUTPUT_FILE]
               [-k [KEY ...]] [-i]

Allows inspecting the data flowing through the pipeline.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m {interactive,non-interactive}, --mode {interactive,non-interactive}
                        The mode to operate in. (default: interactive)
  -o {stdout,stderr,logger,file}, --output {stdout,stderr,logger,file}
                        How to output the data. (default: stdout)
  --output_file OUTPUT_FILE
                        The file to store the data in, in case of output
                        'file'. (default: None)
  -k [KEY ...], --meta-data-key [KEY ...]
                        The meta-data value to output (default: None)
  -i, --show_image      Whether to display the image. (default: False)
```
