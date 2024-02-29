# inspect

* accepts: seppl.AnyData
* generates: seppl.AnyData

Allows inspecting the data flowing through the pipeline.

```
usage: inspect [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
               [-m {interactive,non-interactive}]
               [-o {stdout,stderr,logger,file}] [--output_file OUTPUT_FILE]
               [-k [KEY [KEY ...]]] [-i]

Allows inspecting the data flowing through the pipeline.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -m {interactive,non-interactive}, --mode {interactive,non-interactive}
                        The mode to operate in. (default: interactive)
  -o {stdout,stderr,logger,file}, --output {stdout,stderr,logger,file}
                        How to output the data. (default: stdout)
  --output_file OUTPUT_FILE
                        The file to store the data in, in case of output
                        'file'. (default: None)
  -k [KEY [KEY ...]], --meta-data-key [KEY [KEY ...]]
                        The meta-data value to output (default: None)
  -i, --show_image      Whether to display the image. (default: False)
```
