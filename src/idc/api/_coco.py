import numpy as np
from datetime import datetime
from typing import List, Dict

from idc.api import get_object_label, ObjectDetectionData, ImageSegmentationData
from pycocotools import mask as maskUtils


class COCOAnnotations:
    """
    Container object for collecting MS COCO annotations.
    """

    def __init__(self, image_lookup: Dict[str, int], category_lookup: Dict[str, int],
                 license_name: str = "default", license_url: str = "",
                 error_on_new_category: bool = False, default_supercategory: str = "Object",
                 default_score: float = 1.0):
        """
        Initializes the COCO annotations structure.

        :param image_lookup: the lookup to use/update
        :type image_lookup: dict
        :param category_lookup: the predefined lookup to use/update
        :type category_lookup: dict
        :param license_name: the name of the license
        :type license_name: str
        :param license_url: the URL for the license
        :type license_url: str
        :param error_on_new_category: whether to raise an exception if an unknown category is encountered
        :type error_on_new_category: bool
        :param default_supercategory: the default category
        :type default_supercategory: str
        :param default_score: the default score to use if not present in the annotations
        :type default_score: float
        """
        self.image_lookup = image_lookup
        self.category_lookup = category_lookup
        self.error_on_new_category = error_on_new_category
        self.default_supercategory = default_supercategory
        self.default_score = default_score
        self.license_name = license_name
        self.license_url = license_url
        self.data = dict()
        self._init_annotations()

    def _init_annotations(self):
        """
        Initializes the data structure.
        """
        self.data["info"] = self._create_info()
        self.data["licenses"] = self._create_licenses()
        self.data["images"] = list()
        self.data["annotations"] = list()
        self.data["categories"] = list()

    def _create_info(self) -> Dict:
        """
        Creates the info section.

        :return: the info section
        :rtype: dict
        """
        result = dict()
        result["year"] = datetime.now().strftime("%Y")
        result["version"] = ""
        result["description"] = "Converted with image-dataset-converter"
        result["contributor"] = ""
        result["url"] = ""
        result["date_created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return result

    def _create_licenses(self) -> List:
        """
        Creates the licenses section.

        :return: the licenses section
        :rtype: list
        """
        result = list()
        result.append(dict())
        result[0]["id"] = 1
        result[0]["name"] = self.license_name
        result[0]["url"] = self.license_url
        return result

    def _create_categories(self) -> List:
        """
        Creates the categories section.

        :return: the categories section
        :rtype: list
        """
        result = list()
        for category_name, category_id in self.category_lookup.items():
            category = dict()
            category["id"] = category_id
            category["name"] = category_name
            category["supercategory"] = self.default_supercategory
            result.append(category)
        return result

    def append_image(self, item):
        """
        Appends the image to the images section.

        :param item: the image to append
        """
        image_id = len(self.data["images"]) + 1
        self.image_lookup[item.image_name] = image_id
        image = dict()
        image["id"] = image_id
        image["width"] = item.image_width
        image["height"] = item.image_height
        image["file_name"] = item.image_name
        image["license"] = 1
        image["flickr_url"] = ""
        image["coco_url"] = ""
        image["date_captured"] = ""
        self.data["images"].append(image)

    def append_annotations(self, item):
        """
        Appends the annotations to the annotations section.

        :param item: the image to append
        """
        image_id = self.image_lookup[item.image_name]
        if isinstance(item, ObjectDetectionData):
            absolute = item.get_absolute()
            for obj in absolute:
                label = get_object_label(obj)
                if label not in self.category_lookup:
                    if self.error_on_new_category:
                        raise Exception("Undefined label encountered with image %s: %s" % (item.image_name, label))
                    self.category_lookup[label] = len(self.category_lookup) + 1
                category_id = self.category_lookup[label]
                annotation_id = len(self.data["annotations"]) + 1
                annotation = dict()
                annotation["id"] = annotation_id
                annotation["image_id"] = image_id
                annotation["category_id"] = category_id
                annotation["score"] = float(obj.metadata["score"]) if ("score" in obj.metadata) else self.default_score
                annotation["bbox"] = [obj.x, obj.y, obj.width, obj.height]
                annotation["iscrowd"] = 0
                if obj.has_polygon():
                    annotation["area"] = float(obj.get_actual_polygon().area())
                    x_list = obj.get_polygon_x()
                    y_list = obj.get_polygon_y()
                else:
                    annotation["area"] = float(obj.width * obj.height)
                    x_list = [obj.x, obj.x + obj.width - 1, obj.x + obj.width - 1, obj.x]
                    y_list = [obj.y, obj.y, obj.y + obj.height - 1, obj.y + obj.height - 1]
                segmentation = []
                for x, y in zip(x_list, y_list):
                    segmentation.append(x)
                    segmentation.append(y)
                annotation["segmentation"] = [segmentation]
                self.data["annotations"].append(annotation)
        elif isinstance(item, ImageSegmentationData):
            for label in item.annotation.layers:
                if label not in self.category_lookup:
                    if self.error_on_new_category:
                        raise Exception("Undefined label encountered with image %s: %s" % (item.image_name, label))
                    self.category_lookup[label] = len(self.category_lookup) + 1
                layer = item.annotation.layers[label]
                category_id = self.category_lookup[label]
                annotation_id = len(self.data["annotations"]) + 1
                annotation = dict()
                annotation["id"] = annotation_id
                annotation["image_id"] = image_id
                annotation["category_id"] = category_id
                annotation["score"] = self.default_score
                annotation["iscrowd"] = 0
                rle_mask = maskUtils.encode(np.asfortranarray(layer))
                annotation["segmentation"] = {
                    "size": rle_mask["size"],
                    "counts": rle_mask["counts"].decode("utf-8") if isinstance(rle_mask["counts"], bytes) else rle_mask["counts"]
                }
                annotation["bbox"] = maskUtils.toBbox(rle_mask).tolist()
                annotation["area"] = int(maskUtils.area(rle_mask))
                self.data["annotations"].append(annotation)
        else:
            raise Exception("Unsupported data structure: %s" % str(type(item)))

    def finalize(self):
        """
        Finalizes the annotations, ie compiles the categories.
        """
        self.data["categories"] = self._create_categories()
