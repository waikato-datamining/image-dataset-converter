Changelog
=========

0.0.9 (2025-03-14)
------------------

- using `wai_logging` instead of `wai.logging` as dependency now


0.0.8 (2025-03-14)
------------------

- requiring seppl>=0.2.13 now for placeholder support
- added placeholder support to tools: `idc-convert`, `idc-exec`
- added placeholder support to readers: `from-adams-ic`, `from-subdir-ic`, `from-blue-channel-is`, `from-grayscale-is`,
  `from-indexed-png-is`, `from-layer-segments-is`, `from-adams-od`, `from-coco-od`, `from-opex-od`, `from-roicsv-od`,
  `from-voc-od`, `from-yolo-od`, `from-data`, `from-pyfunc`, `poll-dir`
- added placeholder support to filters: `write-labels`
- added placeholder support to writers: `to-adams-ic`, `to-subdir-ic`, `to-blue-channel-is`, `to-grayscale-is`,
  `to-indexed-png-is`, `to-layer-segments-is`, `to-adams-od`, `to-coco-od`, `to-opex-od`, `to-roicsv-od`,
  `to-voc-od`, `to-yolo-od`, `to-data`


0.0.7 (2025-03-12)
------------------

- added `safe_deepcopy` method to idc.api._utils which creates a deep copy of an object if not None
- added `rgb-to-grayscale` filter to convert color images into gray scale ones
- added `sort-pixels` filter for grayscale images
- the following filters can operate on lists of records now as well: `inspec`, `metadata`, `metadata-from-name`
- added `metadata-od` filter for filtering object-detection annotations based on their meta-data
  (e.g., scores from model predictions)
- the filters `discard-negatives` and `discard-invalid-images` now output how many were discarded/kept
  when processing finishes


0.0.6 (2025-02-26)
------------------

- `LayerSegmentsImageSegmentationReader` now suggest using `--lenient` flag in exception in case image not binary
- added the `discard-by-name` filter that allows user to discard images based on name, either exact match of regexp
  (matching sense can be inverted)
- requiring seppl>=0.2.10 now
- added support for aliases
- added `to_bluechannel`, `to_grayscale` and `to_indexedpng` image segmentation methods to `idc.api`
- added the `generate_palette_list` method to `idc.api` which turns a predefined palette name or comma-separated
  list of RGB values into a flat list of int values, e.g., used for indexed PNG files
- exposed method `save_image` through `idc.api`
- `filter-labels` now handles not specifying any labels and only regexp
- `write-labels` filter now allows specification of custom separator
- `write-labels`: fixed retrieval of image-segmentation labels
- using `simple_palette_utils` dependency now
- `idc-convert` tool now flags aliases on the help screen with `*`
- the `from-voc-od` reader now has the `-r/--image_rel_path` option which gets injected before the `folder` property
  from the XML file


0.0.5 (2025-01-13)
------------------

- added `setuptools` as dependency
- switched to underscores in project name
- using 90% as default quality for JPEG images now, can be overridden with environment variable `IDC_JPEG_QUALITY`
- added methods to idc.api module: `jpeg_quality()`, `array_to_image(...)`, `empty_image(...)`


0.0.4 (2024-07-16)
------------------

- limiting numpy to <2.0.0 due to problems with imgaug library


0.0.3 (2024-07-02)
------------------

- switched to the `fast-opex` library
- helper method `from_indexedpng` was using incorrect label index (off by 1)
- `Data.save_image` method now ensures that source/target files exist before calling `os.path.samefile`
- requiring seppl>=0.2.6 now
- readers now support default globs, allowing the user to just specify directories as input
  (and the default glob gets appended)
- the `to-yolo-od` writer now has an option for predefined labels (for enforcing label order)
- the `to-yolo-od` writer now stores the labels/labels_cvs files in the respective output folders
  rather than using an absolute file name
- the bluechannel/grayscale/indexed-png image segmentation readers/writers can use a value other
  than 0 now for the background
- `split` filter has been renamed to `split-records`


0.0.2 (2024-06-13)
------------------

- added generic plugins that take user Python functions: `from-pyfunc`, `pyfunc-filter`, `to-pyfunc`
- added `idc-exec` tool that uses generator to produce variable/value pairs that are used to expand
  the provided pipeline template which then gets executed
- added `polygon-simplifier` filter for reducing number of points in polygons
- moved several geometry/image related functions from imgaug library into core library to avoid duplication
- added python-image-complete as dependency
- the `ImageData` class now uses the python-image-complete library to determine the file format rather than
  loading the image into memory in order to determine that
- the `convert-image-format` filter now correctly creates a new container with the converted image data
- the `to-coco-od` writer only allows sorting of categories when using predefined categories now
- the `from-opex-od` reader now handles absent meta-data correctly
- added the `AnnotationsOnlyWriter` mixin for writers that can skip the base image and just output the annotations


0.0.1 (2024-05-06)
------------------

- initial release

