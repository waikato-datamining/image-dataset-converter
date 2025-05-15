from ._depth import DepthData
from ._imgcls import ImageClassificationData
from ._imgseg import ImageSegmentationData
from ._objdet import ObjectDetectionData


DATATYPE_DEPTH = "dp"
DATATYPE_IMGCLS = "ic"
DATATYPE_IMGSEG = "is"
DATATYPE_OBJDET = "od"
DATATYPES = [
    DATATYPE_DEPTH,
    DATATYPE_IMGCLS,
    DATATYPE_IMGSEG,
    DATATYPE_OBJDET,
]

DATATYPES_LONG = {
    DATATYPE_DEPTH: "depth",
    DATATYPE_IMGCLS: "image classification",
    DATATYPE_IMGSEG: "image segmentation",
    DATATYPE_OBJDET: "object detection",
}


class DataTypeSupporter:
    """
    Mixin for classes that make use of data types.
    Implementing classes have extra information output on their help screens.
    """
    pass


def data_type_to_class(data_type: str):
    """
    Turns the data type into a class.

    :param data_type: the data type to convert
    :type data_type: str
    :return: the corresponding class
    """
    if data_type == DATATYPE_DEPTH:
        return DepthData
    elif data_type == DATATYPE_IMGCLS:
        return ImageClassificationData
    elif data_type == DATATYPE_IMGSEG:
        return ImageSegmentationData
    elif data_type == DATATYPE_OBJDET:
        return ObjectDetectionData
    else:
        raise Exception("Unsupported data type: %s" % data_type)


def data_types_help(markdown: bool = False) -> str:
    """
    Generates a help string for the data types.

    :param markdown: whether to generate markdown
    :type markdown: bool
    :return: the generated help string
    :rtype: str
    """
    result = "The following data types are available:\n"

    if markdown:
        result += "\n"
        for t in DATATYPES:
            result += "* %s: %s\n" % (t, DATATYPES_LONG[t])
    else:
        for t in DATATYPES:
            result += "- %s: %s\n" % (t, DATATYPES_LONG[t])

    return result
