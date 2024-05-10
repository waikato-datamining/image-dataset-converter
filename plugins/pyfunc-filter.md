# pyfunc-filter

* accepts: idc.api.ImageData
* generates: idc.api.ImageData

The declared Python function processes image containers of the specified input type and generates ones of the specified output type. The function must handle a single image container or an iterable of image containers and return a single image container or an iterable of image containers.

```
usage: pyfunc-filter [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] -i {ic,is,od} -f FUNCTION -o {ic,is,od}

The declared Python function processes image containers of the specified input
type and generates ones of the specified output type. The function must handle
a single image container or an iterable of image containers and return a
single image container or an iterable of image containers.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i {ic,is,od}, --input_data_type {ic,is,od}
                        The type of data to receive (default: None)
  -f FUNCTION, --function FUNCTION
                        The Python function to use, format:
                        module_name:function_name (default: None)
  -o {ic,is,od}, --output_data_type {ic,is,od}
                        The type of data to forward (default: None)
```
