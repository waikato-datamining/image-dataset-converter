Changelog
=========

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

