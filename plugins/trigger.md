# trigger

* accepts: seppl.AnyData
* generates: seppl.AnyData

Triggers the sub-flow with its reader/filter(s)/writer whenever data is passing through. When supplying a meta-data field and a value, this can be turned into a conditional execution, but only when receiving individual objects, not batches of objects. Performs the following comparison: METADATA_VALUE COMPARISON VALUE.

```
usage: trigger [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
               [--skip] [-f SUB_FLOW] [-F {cmdline,file}] [--field FIELD]
               [--comparison {lt,le,eq,ne,ge,gt,contains,matches}]
               [--value VALUE]

Triggers the sub-flow with its reader/filter(s)/writer whenever data is
passing through. When supplying a meta-data field and a value, this can be
turned into a conditional execution, but only when receiving individual
objects, not batches of objects. Performs the following comparison:
METADATA_VALUE COMPARISON VALUE.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f SUB_FLOW, --sub_flow SUB_FLOW
                        The subflow to execute (reader/filter(s)/writer).
                        (default: None)
  -F {cmdline,file}, --sub_flow_format {cmdline,file}
                        The format of the pipeline. (default: cmdline)
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
```
