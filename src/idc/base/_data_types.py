from ._imgcls import ImageClassificationData
from ._imgseg import ImageSegmentationData
from ._objdet import ObjectDetectionData


DATATYPE_IMGCLS = "ic"
DATATYPE_IMGSEG = "is"
DATATYPE_OBJDET = "od"
DATATYPES = [
    DATATYPE_IMGCLS,
    DATATYPE_IMGSEG,
    DATATYPE_OBJDET,
]


def data_type_to_class(data_type: str):
    if data_type == DATATYPE_IMGCLS:
        return ImageClassificationData
    elif data_type == DATATYPE_IMGSEG:
        return ImageSegmentationData
    elif data_type == DATATYPE_OBJDET:
        return ObjectDetectionData
    else:
        raise Exception("Unsupported data type: %s" % data_type)
