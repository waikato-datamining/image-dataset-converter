# annotations-to-metadata

* accepts: seppl.AnyData
* generates: seppl.AnyData

Stores the annotations in the metadata under the specified field.

```
usage: annotations-to-metadata [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                               [-N LOGGER_NAME] [--skip] [-s METADATA_KEY]

Stores the annotations in the metadata under the specified field.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s METADATA_KEY, --metadata_key METADATA_KEY
                        The field to store the annotations under in the meta-
                        data. (default: annotations)
```
