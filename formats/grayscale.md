# Grayscale

## Depth data

The depth information is stored as grayscale value. The actual range of values 
of the depth information is scaled to 0-255. When loading, the range can be
changed again.

**NB:** Lossy format for depth information.


## Image segmentation

These annotations for image segmentation are available through PNG or JPG files. 
The grayscale value is equivalent to the index of the label. 
0 is typically considered to be the background.
