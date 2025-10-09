# attach-metadata

* accepts: seppl.AnyData
* generates: seppl.AnyData

Attaches meta-data to the data passing through. Loads the data from the specified directory based on the data's name. In case of CSV, a header row is expected and the first column contains the keys and the second the values.

```
usage: attach-metadata [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] -m METADATA_DIR
                       [-f {csv,json}]

Attaches meta-data to the data passing through. Loads the data from the
specified directory based on the data's name. In case of CSV, a header row is
expected and the first column contains the keys and the second the values.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m METADATA_DIR, --metadata_dir METADATA_DIR
                        The directory with the meta-data files to load/attach.
                        (default: None)
  -f {csv,json}, --metadata_format {csv,json}
                        The format of the meta-data. (default: json)
```
