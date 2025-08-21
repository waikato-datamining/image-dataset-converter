# csv-file

Forwards the values in the columns of the CSV file, using the column headers as variable names.

```
usage: csv-file [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                -f FILE

Forwards the values in the columns of the CSV file, using the column headers
as variable names.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -f FILE, --csv_file FILE
                        The CSV file to use. (default: None)
```
