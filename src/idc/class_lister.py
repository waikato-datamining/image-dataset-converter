from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "idc.reader",
            "idc.reader.imgcls",
            "idc.reader.imgseg",
            "idc.reader.objdet",
        ],
        "seppl.io.Filter": [
            "idc.filter",
            "idc.filter.imgcls",
            "idc.filter.imgseg",
            "idc.filter.objdet",
        ],
        "seppl.io.Writer": [
            "idc.writer",
            "idc.writer.imgcls",
            "idc.writer.imgseg",
            "idc.writer.objdet",
        ],
        "idc.api.Generator": [
            "idc.generator",
        ],
    }
