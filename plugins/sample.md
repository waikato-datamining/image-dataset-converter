# sample

* accepts: seppl.AnyData
* generates: seppl.AnyData

Selects a sub-sample from the stream.

```
usage: sample [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [--skip] [-s SEED] [-T THRESHOLD]

Selects a sub-sample from the stream.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s SEED, --seed SEED  The seed value to use for the random number generator;
                        randomly seeded if not provided. (default: None)
  -T THRESHOLD, --threshold THRESHOLD
                        The threshold to use for Random.rand(): if equal or
                        above, sample gets selected; range: 0-1; 0 = always.
                        (default: 0.0)
```
