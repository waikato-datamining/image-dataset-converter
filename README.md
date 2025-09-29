# image-dataset-converter
For converting image annotations datasets from one format into another.
Filters can be supplied as well, e.g., for cleaning up the data.

[Additional libraries](#additional-libraries) further extend the available
plugins with additional readers, filters and/or writers.


## Installation

Via PyPI:

```bash
pip install image_dataset_converter
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-datamining/image-dataset-converter.git
```


## Docker

Docker images are available as well. Please see the following page por more information:

https://github.com/waikato-datamining/image-dataset-converter-all/tree/main/docker


## Dataset formats

The following dataset formats are supported:

| Domain                 | Format                                                                        | Read                                   | Write                                | 
|:-----------------------|:------------------------------------------------------------------------------|:---------------------------------------|:-------------------------------------| 
| Depth data             | [CSV](formats/csv.md)                                                         | [Y](plugins/from-csv-dp.md)            | [Y](plugins/to-csv-dp.md)            | 
| Depth data             | [Grayscale](formats/grayscale.md)                                             | [Y](plugins/from-grayscale-dp.md)      | [Y](plugins/to-grayscale-dp.md)      | 
| Depth data             | [Numpy](formats/numpy.md)                                                     | [Y](plugins/from-numpy-dp.md)          | [Y](plugins/to-numpy-dp.md)          | 
| Depth data             | [PFM](formats/pfm.md)                                                         | [Y](plugins/from-pfm-dp.md)            | [Y](plugins/to-pfm-dp.md)            | 
| Image classification   | [ADAMS](formats/adams.md)                                                     | [Y](plugins/from-adams-ic.md)          | [Y](plugins/to-adams-ic.md)          | 
| Image classification   | [subdir](formats/subdir.md)                                                   | [Y](plugins/from-subdir-ic.md)         | [Y](plugins/to-subdir-ic.md)         | 
| Image segmentation     | [Blue-channel](formats/bluechannel.md)                                        | [Y](plugins/from-blue-channel-is.md)   | [Y](plugins/to-blue-channel-is.md)   | 
| Image segmentation     | [Grayscale](formats/grayscale.md)                                             | [Y](plugins/from-grayscale-is.md)      | [Y](plugins/to-grayscale-is.md)      | 
| Image segmentation     | [Indexed PNG](formats/indexedpng.md)                                          | [Y](plugins/from-indexed-png-is.md)    | [Y](plugins/to-indexed-png-is.md)    | 
| Image segmentation     | [Layer segments](formats/layersegments.md)                                    | [Y](plugins/from-layer-segments-is.md) | [Y](plugins/to-layer-segments-is.md) | 
| Object detection       | [ADAMS](formats/adams.md)                                                     | [Y](plugins/from-adams-od.md)          | [Y](plugins/to-adams-od.md)          | 
| Object detection       | [COCO](https://cocodataset.org/#format-data)                                  | [Y](plugins/from-coco-od.md)           | [Y](plugins/to-coco-od.md)           | 
| Object detection       | [OPEX](https://github.com/WaikatoLink2020/objdet-predictions-exchange-format) | [Y](plugins/from-opex-od.md)           | [Y](plugins/to-opex-od.md)           | 
| Object detection       | [ROI CSV](formats/roicsv.md)                                                  | [Y](plugins/from-roicsv-od.md)         | [Y](plugins/to-roicsv-od.md)         | 
| Object detection       | [VOC](formats/voc.md)                                                         | [Y](plugins/from-voc-od.md)            | [Y](plugins/to-voc-od.md)            | 
| Object detection       | [YOLO](formats/yolo.md)                                                       | [Y](plugins/from-yolo-od.md)           | [Y](plugins/to-yolo-od.md)           | 


## Domain suffixes

Readers and writers typically have a suffix that denotes their data domain:

* `-dp` - Depth data
* `-ic` - Image classification
* `-is` - Image segmentation 
* `-od` - Object detection 


## Tools

### Dataset conversion

```
usage: idc-convert [-h] [--help-all] [--help-plugin NAME] [-u INTERVAL]
                   [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-b]
                   [--placeholders FILE] [--load_pipeline FILE]
                   [--dump_pipeline FILE]

Tool for converting between image annotation dataset formats.

readers (26):
   from-adams-ic, from-adams-od, from-blue-channel-is, from-coco-od, 
   from-csv-dp, from-data, from-grayscale-dp, from-grayscale-is, 
   from-indexed-png-is, from-layer-segments-is, from-multi, 
   from-numpy-dp, from-opex-od, from-pfm-dp, from-pyfunc, 
   from-roicsv-od, from-storage, from-subdir-ic, from-text-file, 
   from-voc-od, from-yolo-od, get-email, list-files, poll-dir, start, 
   watch-dir
filters (60):
   any-to-rgb, apply-ext-mask, apply-label-mask, block, 
   check-duplicate-filenames, coerce-box, coerce-mask, 
   convert-image-format, copy-files, count-specks, depth-to-grayscale, 
   depth-to-greyscale*, dimension-discarder, dims-to-metadata, 
   discard-by-name, discard-invalid-images, discard-negatives, 
   filter-labels, grayscale-to-binary, greyscale-to-binary*, inspect, 
   label-from-name, label-present*, label-present-ic, label-present-is, 
   label-present-od, label-to-metadata, list-to-sequence, map-labels, 
   max-records, metadata, metadata-from-name, metadata-od, 
   metadata-to-placeholder, move-files, od-to-ic, od-to-is, passthrough, 
   polygon-discarder, polygon-simplifier, pyfunc-filter, 
   randomize-records, record-window, remove-classes, rename, 
   rgb-to-grayscale, rgb-to-greyscale*, sample, set-metadata, 
   set-placeholder, set-storage, sort-pixels, split-records, stop, 
   strip-annotations, sub-process, tee, trigger, use-mask, write-labels
writers (24):
   console, delete-files, send-email, to-adams-ic, to-adams-od, 
   to-blue-channel-is, to-coco-od, to-csv-dp, to-data, to-grayscale-dp, 
   to-grayscale-is, to-indexed-png-is, to-layer-segments-is, to-multi, 
   to-numpy-dp, to-opex-od, to-pfm-dp, to-pyfunc, to-roicsv-od, 
   to-storage, to-subdir-ic, to-text-file, to-voc-od, to-yolo-od

options:
  -h, --help           Show basic help message and exit.
  --help-all           Show basic help message plus help on all plugins and exit.
  --help-plugin NAME   Show help message for plugin NAME and exit.
  -u, --update_interval INTERVAL
                       Outputs the progress every INTERVAL records (default: 1000).
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                       The logging level to use (default: WARN).
  -b, --force_batch    Processes the data in batches.
  --placeholders FILE  The file with custom placeholders to load (format: key=value).
  --load_pipeline FILE The file to load the pipeline command from.
  --dump_pipeline FILE The file to dump the pipeline command in.
```

### Executing pipeline multiple times

```
usage: idc-exec [-h] --exec_generator GENERATOR [--exec_dry_run]
                [--exec_prefix PREFIX] [--exec_placeholders FILE]
                [--exec_format {cmdline,file}]
                [--exec_logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                ...

Tool for executing a pipeline multiple times, each time with a different set
of variables expanded. A variable is surrounded by curly quotes (e.g.,
variable 'i' gets referenced with '{i}'). When supplying multiple generators,
then these get treated as nested executions. Available generators: csv-file,
dirs, list, null, prompt, range, text-file

positional arguments:
  pipeline              The pipeline template with variables to expand and
                        then execute; see '--exec_format' option.

options:
  -h, --help            show this help message and exit
  --exec_generator GENERATOR
                        The generator plugin(s) to use, incl. their options.
                        Flag needs to be specified for each generator.
                        (default: None)
  --exec_dry_run        Applies the generator to the pipeline template and
                        only outputs it on stdout. (default: False)
  --exec_prefix PREFIX  The string to prefix the pipeline with when in dry-run
                        mode. (default: None)
  --exec_placeholders FILE
                        The file with custom placeholders to load (format:
                        key=value). (default: None)
  --exec_format {cmdline,file}
                        The format that the pipeline is in. The format
                        'cmdline' interprets the remaining arguments as the
                        pipeline arguments to execute. The format 'file'
                        expects a file to load the pipeline arguments from.
                        This file format allows spreading the pipeline
                        arguments over multiple lines: it simply joins all
                        lines into a single command-line before splitting it
                        into individual arguments for execution. (default:
                        cmdline)
  --exec_logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Locating files

Readers tend to support input via file lists. The `idc-find` tool can generate
these.

```
usage: idc-find [-h] -i DIR [DIR ...] [-r] -o FILE [-m [REGEXP ...]]
                [-n [REGEXP ...]] [--split_ratios [SPLIT_RATIOS ...]]
                [--split_names [SPLIT_NAMES ...]]
                [--split_name_separator SPLIT_NAME_SEPARATOR]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for locating files in directories that match certain patterns and store
them in files.

options:
  -h, --help            show this help message and exit
  -i DIR [DIR ...], --input DIR [DIR ...]
                        The dir(s) to scan for files. (default: None)
  -r, --recursive       Whether to search the directories recursively
                        (default: False)
  -o FILE, --output FILE
                        The file to store the located file names in (default:
                        None)
  -m [REGEXP ...], --match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be included (default: None)
  -n [REGEXP ...], --not-match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be excluded (default: None)
  --split_ratios [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (int; must sum up to 100) (default: None)
  --split_names [SPLIT_NAMES ...]
                        The split names to use as filename suffixes for the
                        generated splits (before .ext) (default: None)
  --split_name_separator SPLIT_NAME_SEPARATOR
                        The separator to use between file name and split name
                        (default: -)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Generating help screens for plugins

```
usage: idc-help [-h] [-c [PACKAGE ...]] [-e EXCLUDED_CLASS_LISTERS]
                [-T {pipeline,generator}] [-p NAME] [-f {text,markdown}]
                [-L INT] [-o PATH] [-i FILE] [-t TITLE]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for outputting help for plugins in various formats.

options:
  -h, --help            show this help message and exit
  -c [PACKAGE ...], --custom_class_listers [PACKAGE ...]
                        The custom class listers to use, uses the default ones
                        if not provided. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -T {pipeline,generator}, --plugin_type {pipeline,generator}
                        The types of plugins to generate the help for.
                        (default: pipeline)
  -p NAME, --plugin_name NAME
                        The name of the plugin to generate the help for,
                        generates it for all if not specified (default: None)
  -f {text,markdown}, --help_format {text,markdown}
                        The output format to generate (default: text)
  -L INT, --heading_level INT
                        The level to use for the heading (default: 1)
  -o PATH, --output PATH
                        The directory or file to store the help in; outputs it
                        to stdout if not supplied; if pointing to a directory,
                        automatically generates file name from plugin name and
                        help format (default: None)
  -i FILE, --index_file FILE
                        The file in the output directory to generate with an
                        overview of all plugins, grouped by type (in markdown
                        format, links them to the other generated files)
                        (default: None)
  -t TITLE, --index_title TITLE
                        The title to use in the index file (default: image-
                        dataset-converter plugins)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Plugin registry

```
usage: idc-registry [-h] [-c CUSTOM_CLASS_LISTERS] [-e EXCLUDED_CLASS_LISTERS]
                    [-l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}]

For inspecting/querying the registry.

options:
  -h, --help            show this help message and exit
  -c CUSTOM_CLASS_LISTERS, --custom_class_listers CUSTOM_CLASS_LISTERS
                        The comma-separated list of custom class listers to
                        use. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}, --list {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}
                        For outputting various lists on stdout. (default:
                        None)
```

### Testing generators

```
usage: idc-test-generator [-h] -g GENERATOR
                          [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for testing generators by outputting the generated variables and their
associated values. Available generators: csv-file, dirs, list, null, prompt,
range, text-file

options:
  -h, --help            show this help message and exit
  -g GENERATOR, --exec_generator GENERATOR
                        The generator plugin(s) to use, incl. their options.
                        Flag needs to be specified for each generator.
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


## Plugins

You can find help screens for the plugins here:

* [Pipeline plugins](plugins/README.md) (readers/filters/writers)
* [Generator plugins](generators/README.md) (used by `idc-exec`)


## Command-line examples

Examples can be found on the [image-dataset-converter-examples](https://www.data-mining.co.nz/image-dataset-converter-examples/)
website.


## Class listers

The *image-dataset-converter* uses the *class lister registry* provided 
by the [seppl](https://github.com/waikato-datamining/seppl) library.

Each module defines a function, typically called `list_classes` that returns
a dictionary of names of superclasses associated with a list of modules that
should be scanned for derived classes. Here is an example:

```python
from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "mod.ule1",
            "mod.ule2",
        ],
        "seppl.io.Filter": [
            "mod.ule3",
            "mod.ule4",
        ],
        "seppl.io.Writer": [
            "mod.ule5",
        ],
    }
```

Such a class lister gets referenced in the `entry_points` section of the `setup.py` file:

```python
    entry_points={
        "class_lister": [
            "unique_string=module_name:function_name",
        ],
    },
```

`:function_name` can be omitted if `:list_classes`.

The following environment variables can be used to influence the class listers:

* `IDC_CLASS_LISTERS`
* `IDC_CLASS_LISTERS_EXCL`
* `IDC_CLASS_LISTERS_IGNORED` - for class listers that provide ignored classes

Each variable is a comma-separated list of `module_name:function_name`, defining the class listers.


## JPEG quality

Whenever possible, images get copied rather than read and then rewritten, 
to avoid loss of quality by subsequent read/write operations.
To minimize introduction of artifacts in JPEG images, a default quality of 90% 
is used, which is a good compromise between size and quality. 

However, this quality parameter can be overridden globally with the following 
environment variable:

```
IDC_JPEG_QUALITY
```

For instance, the following setting would use a quality of 100%: 

```
IDC_JPEG_QUALITY=100
```


## Caching plugins

In order to speed up plugin discovery, they discovered plugins can be cached
on disk after the initial discovery. Installing additional plugins after
the cache has been initialized will not make them visible, the cache will
require resetting first.

The cache can be managed through the following environment variable:

```
IDC_CLASS_CACHE
```

It supports the following options:

* `off`: disables the cache
* `on`: enables the cache
* `reset`: resets the cached plugins first and enables the cache


## Additional libraries

* [Image augmentation](https://github.com/waikato-datamining/image-dataset-converter-imgaug)
* [Image statistics](https://github.com/waikato-datamining/image-dataset-converter-imgstats)
* [Image visualizations](https://github.com/waikato-datamining/image-dataset-converter-imgvis)
* [labelme](https://github.com/waikato-datamining/image-dataset-converter-labelme)
* [Paddle](https://github.com/waikato-datamining/image-dataset-converter-paddle)
* [PDF](https://github.com/waikato-datamining/image-dataset-converter-pdf)
* [PlantCV](https://github.com/waikato-datamining/image-dataset-converter-plantcv)
* [Redis](https://github.com/waikato-datamining/image-dataset-converter-redis)
* [Video](https://github.com/waikato-datamining/image-dataset-converter-video)
