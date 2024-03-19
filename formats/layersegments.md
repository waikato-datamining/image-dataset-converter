# Layer segments

This image segmentation format separates the various labels into separate layers.
Each layer is a binary PNG image, with black being the background and white the
object annotations.

The label name is encoded in the filename, typically as a suffix. Here is an example:

```
IMAGE.jpg
IMAGE-LABEL1.png
IMAGE-LABEL2.png
IMAGE-LABEL3.png
```
