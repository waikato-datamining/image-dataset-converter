from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "kasperl.reader",
            "idc.reader",
            "idc.reader.depth",
            "idc.reader.imgcls",
            "idc.reader.imgseg",
            "idc.reader.objdet",
        ],
        "seppl.io.Filter": [
            "kasperl.filter",
            "idc.filter",
            "idc.filter.depth",
            "idc.filter.imgcls",
            "idc.filter.imgseg",
            "idc.filter.objdet",
        ],
        "seppl.io.Writer": [
            "kasperl.writer",
            "idc.writer",
            "idc.writer.depth",
            "idc.writer.imgcls",
            "idc.writer.imgseg",
            "idc.writer.objdet",
        ],
        "kasperl.api.Generator": [
            "kasperl.generator",
        ],
    }
