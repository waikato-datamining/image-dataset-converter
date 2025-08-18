# check-duplicate-filenames

* accepts: seppl.AnyData
* generates: seppl.AnyData

Ensures that file names are unique (raises an exception if not).

```
usage: check-duplicate-filenames [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                                 [-N LOGGER_NAME] [--skip]
                                 [-a {ignore,warn,drop,error}]

Ensures that file names are unique (raises an exception if not).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -a {ignore,warn,drop,error}, --action {ignore,warn,drop,error}
                        The action to perform when encountering a duplicate
                        file name (default: error)
```
