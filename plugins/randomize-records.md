# randomize-records

* accepts: seppl.AnyData
* generates: seppl.AnyData

Batch filter that randomizes the order of the records.

```
usage: randomize-records [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [-N LOGGER_NAME] [--skip] [-s SEED]

Batch filter that randomizes the order of the records.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s SEED, --seed SEED  The seed value to use for the randomization. Without
                        seed value the order will differ between runs.
                        (default: None)
```
