# ADAMS

[ADAMS](https://adams.cms.waikato.ac.nz/) reports are just [Java .properties](https://en.wikipedia.org/wiki/.properties)
files used for storing meta-data. Since these files do not store any type information, 
ADAMS reports store with each key-value pair of data an additional key-value pair that
contains the type information. As data types, the following are supported:

* `B`: boolean
* `N`: numeric (float or integer)
* `S`: string
* `U`: unknown (treated as string)

The data type appends `<TAB>DataType` to the key of the data pair. Here is an example:

```properties
# comments get ignored
A=some_kind_of_string
A\tDataType=S
B=20.0
B\tDataType=N
C=true
C\tDataType=B
```

In case of **image classification**, a single field in the report will hold the class label.

For **object detection** (bounding box or shape), each object groups its properties via a
common prefix. This is usually `Object.NNN.` with `NNN` an integer index for the object.

As suffixes the following are common:
* `x`: the left of the top-left corner of the bbox
* `y`: the top of the top-left corner of the bbox
* `width`: the width of the bbox
* `height`: the height of the bbox
* `poly_x` (optional): comma-separated list of x coordinates of the shape
* `poly_y` (optional): comma-separated list of y coordinates of the shape

All other suffixes are considered *meta-data* for an object. Object detection usually
stores the *label* in the `type` suffix.
