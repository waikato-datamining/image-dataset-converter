# stop

* accepts: seppl.AnyData
* generates: seppl.AnyData

Raises an exception when the expression evaluates to True, stopping the pipeline. Never raises an exception if no meta-data field specified. Performs the following comparison: METADATA_VALUE COMPARISON VALUE.

```
usage: stop [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
            [--skip] [--field FIELD]
            [--comparison {lt,le,eq,ne,ge,gt,contains,matches}]
            [--value VALUE] [--stop_message STOP_MESSAGE]

Raises an exception when the expression evaluates to True, stopping the
pipeline. Never raises an exception if no meta-data field specified. Performs
the following comparison: METADATA_VALUE COMPARISON VALUE.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --field FIELD         The meta-data field to use in the comparison (default:
                        None)
  --comparison {lt,le,eq,ne,ge,gt,contains,matches}
                        How to compare the value with the meta-data value; lt:
                        less than, le: less or equal, eq: equal, ne: not
                        equal, gt: greater than, ge: greater of equal,
                        contains: substring match, matches: regexp match; in
                        case of 'contains' and 'matches' the supplied value
                        represents the substring to find/regexp to search with
                        (default: eq)
  --value VALUE         The value to use in the comparison (default: None)
  --stop_message STOP_MESSAGE
                        The message to use in the exception. (default: None)
```
