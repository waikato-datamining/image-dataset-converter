Changelog
=========

0.0.2 (????-??-??)
------------------

- added generic plugins that take user Python functions: `from-pyfunc`, `pyfunc-filter`, `to-pyfunc`
- added `idc-exec` tool that uses generator to produce variable/value pairs that are used to expand
  the provided pipeline template which then gets executed
- added `polygon-simplifier` filter for reducing number of points in polygons
- moved functions `shapely_to_locatedobject`, `polygon_to_shapely`, `bbox_to_shapely` from imgaug library
  into core library to avoid duplication


0.0.1 (2024-05-06)
------------------

- initial release

