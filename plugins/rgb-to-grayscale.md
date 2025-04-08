# rgb-to-greyscale

* accepts: idc.api.ImageData
* generates: seppl.AnyData
* alias(es): rgb-to-greyscale

Turns RGB images into grayscale ones.
BT.601: https://en.wikipedia.org/wiki/Rec._601
BT.709: https://en.wikipedia.org/wiki/Rec._709
BT.2020: https://en.wikipedia.org/wiki/Rec._2020

```
usage: rgb-to-grayscale [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [-N LOGGER_NAME] [--skip] [-c {BT.601,BT.709,BT.2020}]

Turns RGB images into grayscale ones. BT.601:
https://en.wikipedia.org/wiki/Rec._601 BT.709:
https://en.wikipedia.org/wiki/Rec._709 BT.2020:
https://en.wikipedia.org/wiki/Rec._2020

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -c {BT.601,BT.709,BT.2020}, --conversion {BT.601,BT.709,BT.2020}
                        The conversion to apply. (default: BT.601)
```
