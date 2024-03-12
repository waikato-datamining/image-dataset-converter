# from-layer-segments-is

* generates: idc.api.ImageSegmentationData

Loads the annotations from associated mask PNG image files, with one binary mask per layer/label.

```
usage: from-layer-segments-is [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                              [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                              [-I [INPUT_LIST [INPUT_LIST ...]]]
                              [--labels LABEL [LABEL ...]]
                              [--label_separator LABEL_SEPARATOR] [--lenient]
                              [--invert]

Loads the annotations from associated mask PNG image files, with one binary
mask per layer/label.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the report file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST [INPUT_LIST ...]], --input_list [INPUT_LIST [INPUT_LIST ...]]
                        Path to the text file(s) listing the text files to use
                        (default: None)
  --labels LABEL [LABEL ...]
                        The labels that the indices represent. (default: None)
  --label_separator LABEL_SEPARATOR
                        The separator between name and label used by the mask
                        images. (default: -)
  --lenient             Will convert non-binary masks with just two unique
                        color values quietly to binary without raising an
                        exception. (default: False)
  --invert              Will invert the binary images (b/w <-> w/b). (default:
                        False)
```
