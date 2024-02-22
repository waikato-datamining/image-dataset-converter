# ROI CSV

Simple, [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) spreadsheet-based annotation 
format, which can either use *top/left and width/height* or *top/left and bottom/right* for 
coordinates (and normalized values). Additionally, it can store polygon coordinates as well. 
That way, it can be used for bounding boxes and shapes alike.

* common columns

  * file: the file name
  * label: the label index (0-based)
  * label_str: the label string
  * score: the prediction score
  * poly_x: the x coordinates of the shape (comma-separated)
  * poly_y: the y coordinates of the shape (comma-separated)
  * poly_xn: the (normalized) x coordinates of the shape (comma-separated)
  * poly_yn: the (normalized) y coordinates of the shape (comma-separated)

* *top/left and width/height* columns

  * x: the left coordinate
  * y: the top coordinate
  * w: the width of the bbox
  * h: the height of the bbox
  * xn: the (normalized) left coordinate
  * yn: the (normalized) top coordinate
  * wn: the (normalized) width of the bbox
  * hn: the (normalized) height of the bbox

* *top/left and bottom/right* columns

  * x0: the left coordinate
  * y0: the top coordinate
  * x1: the right coordinate
  * y1: the bottom coordinate
  * x0n: the (normalized) left coordinate
  * y0n: the (normalized) top coordinate
  * x1n: the (normalized) right coordinate
  * y1n: the (normalized) bottom coordinate