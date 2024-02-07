# image-dataset-converter
For converting image annotations datasets from one format into another.
Filters can be supplied as well, e.g., for cleaning up the data.


## Installation

Via PyPI:

```bash
pip install image-dataset-converter
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-datamining/image-dataset-converter.git
```

## Docker

[Docker](docker) images are available from:

* Docker hub: [waikatodatamining/image-dataset-converter](https://hub.docker.com/r/waikatodatamining/image-dataset-converter)
* In-house registry: `public.aml-repo.cms.waikato.ac.nz:443/tools/image-dataset-converter`



## Dataset formats

The following dataset formats are supported:

| Domain               | Format | Read                           | Write                        | 
|:---------------------|:-------|:-------------------------------|:-----------------------------| 
| Image classification | subdir | [Y](plugins/from-subdir-ic.md) | [Y](plugins/to-subdir-ic.md) | 


## Tools

### Dataset conversion

```
usage: img-convert [-h|--help|--help-all|-help-plugin NAME] [-u INTERVAL]
                   [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   reader
                   [filter [filter [...]]]
                   writer

Tool for converting between image annotation dataset formats.

readers:
   from-subdir-ic
filters:
   strip-annotations
writers:
   to-subdir-ic

optional arguments:
  -h, --help            show basic help message and exit
  --help-all            show basic help message plus help on all plugins and exit
  --help-plugin NAME    show help message for plugin NAME and exit
  -u INTERVAL, --update_interval INTERVAL
                        outputs the progress every INTERVAL records (default: 1000)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        the logging level to use (default: WARN)
  -b, --force_batch     processes the data in batches
```


### Locating files

Readers tend to support input via file lists. The `img-find` tool can generate
these.

```
usage: img-find [-h] -i DIR [DIR ...] [-r] -o FILE [-m [REGEXP [REGEXP ...]]]
                [-n [REGEXP [REGEXP ...]]]
                [--split_ratios [SPLIT_RATIOS [SPLIT_RATIOS ...]]]
                [--split_names [SPLIT_NAMES [SPLIT_NAMES ...]]]
                [--split_name_separator SPLIT_NAME_SEPARATOR]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for locating files in directories that match certain patterns and store
them in files.

optional arguments:
  -h, --help            show this help message and exit
  -i DIR [DIR ...], --input DIR [DIR ...]
                        The dir(s) to scan for files. (default: None)
  -r, --recursive       Whether to search the directories recursively
                        (default: False)
  -o FILE, --output FILE
                        The file to store the located file names in (default:
                        None)
  -m [REGEXP [REGEXP ...]], --match [REGEXP [REGEXP ...]]
                        The regular expression that the (full) file names must
                        match to be included (default: None)
  -n [REGEXP [REGEXP ...]], --not-match [REGEXP [REGEXP ...]]
                        The regular expression that the (full) file names must
                        match to be excluded (default: None)
  --split_ratios [SPLIT_RATIOS [SPLIT_RATIOS ...]]
                        The split ratios to use for generating the splits
                        (int; must sum up to 100) (default: None)
  --split_names [SPLIT_NAMES [SPLIT_NAMES ...]]
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
usage: img-help [-h] [-m [PACKAGE [PACKAGE ...]]] [-e EXCLUDED_MODULES]
                [-p NAME] [-f FORMAT] [-L INT] [-o PATH] [-i FILE]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for outputting help for plugins in various formats.

optional arguments:
  -h, --help            show this help message and exit
  -m [PACKAGE [PACKAGE ...]], --modules [PACKAGE [PACKAGE ...]]
                        The names of the module packages, uses the default
                        ones if not provided. (default: None)
  -e EXCLUDED_MODULES, --excluded_modules EXCLUDED_MODULES
                        The comma-separated list of modules to excluded.
                        (default: None)
  -p NAME, --plugin_name NAME
                        The name of the plugin to generate the help for,
                        generates it for all if not specified (default: None)
  -f FORMAT, --help_format FORMAT
                        The output format to generate (default: text)
  -L INT, --heading_level INT
                        The level to use for the heading (default: 1)
  -o PATH, --output PATH
                        The directory or file to store the help in; outputs it
                        to stdout if not supplied; if pointing to a directory,
                        automatically generates file name from plugin name and
                        help format (default: None)
  -i FILE, --index FILE
                        The file in the output directory to generate with an
                        overview of all plugins, grouped by type (in markdown
                        format, links them to the other generated files)
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Plugin registry

```
usage: img-registry [-h] [-m CUSTOM_MODULES] [-e EXCLUDED_MODULES]
                    [-l {plugins,custom-modules,env-modules,readers,filters,writers}]

For inspecting/querying the registry.

optional arguments:
  -h, --help            show this help message and exit
  -m CUSTOM_MODULES, --custom_modules CUSTOM_MODULES
                        The comma-separated list of custom modules to use.
                        (default: None)
  -e EXCLUDED_MODULES, --excluded_modules EXCLUDED_MODULES
                        The comma-separated list of modules to excluded.
                        (default: None)
  -l {plugins,custom-modules,env-modules,readers,filters,writers}, --list {plugins,custom-modules,env-modules,readers,filters,writers}
                        For outputting various lists on stdout. (default:
                        None)
```


## Plugins

See [here](plugins/README.md) for an overview of all plugins.


## Command-line examples

TODO

