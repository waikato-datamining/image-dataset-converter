# check-polygon-validity

* accepts: idc.api.ObjectDetectionData
* generates: idc.api.ObjectDetectionData

Checks whether the polygons of object annotations are valid and stores the result in the object's meta-data.

```
usage: check-polygon-validity [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                              [-N LOGGER_NAME] [--skip]
                              [-a {record-all,record-invalid,record-valid}]
                              [-f FIELD]

Checks whether the polygons of object annotations are valid and stores the
result in the object's meta-data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -a {record-all,record-invalid,record-valid}, --action {record-all,record-invalid,record-valid}
                        The action to perform when analyzing the validity of
                        polygons. (default: record-all)
  -f FIELD, --field FIELD
                        The object's metadata field for the result of the
                        validity test. (default: polygon_validity)
```
