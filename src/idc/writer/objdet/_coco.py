import argparse
import json
import os
from datetime import datetime
from typing import List, Iterable, Dict

from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, SplittableBatchWriter, get_object_label, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class COCOObjectDetectionWriter(SplittableBatchWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None,
                 license_name: str = "default", license_url: str = "",
                 categories: List[str] = None, error_on_new_category: bool = False,
                 default_supercategory: str = "Object", sort_categories: bool = False,
                 category_output_file: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param license_name: the name of the license to use
        :type license_name: str
        :param license_url: the URL of the license to use
        :type license_url: str
        :param categories: the predefined categories to use
        :type categories: str
        :param error_on_new_category: whether to raise an exception when an unseen category is encountered
        :type error_on_new_category: bool
        :param default_supercategory: the default super category to use, eg Object
        :type default_supercategory: str
        :param sort_categories: whether to sort the categories
        :type sort_categories: bool
        :param category_output_file: the file to store the categories in (comma-separated list)
        :type category_output_file: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir
        self.license_name = license_name
        self.license_url = license_url
        self.categories = categories
        self.error_on_new_category = error_on_new_category
        self.default_supercategory = default_supercategory
        self.sort_categories = sort_categories
        self.category_output_file = category_output_file
        self.annotations_only = annotations_only
        self._category_lookup = None
        self._image_lookup = None
        self._splits = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-coco-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box/polygon definitions in MS COCO .json format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.json files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--license_name", type=str, help="The name of the license to use.", required=False, default="default")
        parser.add_argument("--license_url", type=str, help="The URL of the license to use.", required=False, default="")
        parser.add_argument("--categories", type=str, help="The predefined order of categories.", required=False, nargs="*")
        parser.add_argument("--error_on_new_category", action="store_true", help="Whether to raise an exception if an unknown category is encountered.", required=False)
        parser.add_argument("--default_supercategory", type=str, help="The default super category to use, e.g., 'Object'.", required=False, default="Object")
        parser.add_argument("--sort_categories", action="store_true", help="Whether to sort the categories.", required=False)
        parser.add_argument("--category_output_file", type=str, help="The name of the file (no path) to store the categories in as comma-separated list.", required=False, default=None)
        add_annotations_only_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.license_name = ns.license_name
        self.license_url = ns.license_url
        self.categories = ns.categories
        self.error_on_new_category = ns.error_on_new_category
        self.default_supercategory = ns.default_supercategory
        self.sort_categories = ns.sort_categories
        self.category_output_file = ns.category_output_file
        self.annotations_only = ns.annotations_only

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if self.annotations_only is None:
            self.annotations_only = False

        self._category_lookup = dict()
        if self.categories is not None:
            cats = self.categories
            if self.sort_categories:
                cats = sorted(cats)
            for i, category in enumerate(cats, start=1):
                self._category_lookup[category] = i
        else:
            if self.sort_categories:
                self.logger().warning("Sorting of categories is only supported when using predefined categories!")
                self.sort_categories = False

        self._splits = dict()
        self._image_lookup = dict()

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
        for category_name, category_id in self._category_lookup.items():
            category = dict()
            category["id"] = category_id
            category["name"] = category_name
            category["supercategory"] = self.default_supercategory
            result.append(category)
        return result

    def _init_annotations(self) -> Dict:
        """
        Initializes the annotations structure.
        """
        result = dict()
        result["info"] = self._create_info()
        result["licenses"] = self._create_licenses()
        result["images"] = list()
        result["annotations"] = list()
        result["categories"] = list()
        return result

    def _append_image(self, data: Dict, item):
        """
        Appends the image to the images section.

        :param data: the annotations structure to update
        :type data: dict
        """
        image_id = len(data["images"]) + 1
        self._image_lookup[item.image_name] = image_id
        image = dict()
        image["id"] = image_id
        image["width"] = item.image_width
        image["height"] = item.image_height
        image["file_name"] = item.image_name
        image["license"] = 1
        image["flickr_url"] = ""
        image["coco_url"] = ""
        image["date_captured"] = ""
        data["images"].append(image)

    def _append_annotations(self, data: Dict, item):
        """
        Appends the annotations to the annotations section.

        :param data: the annotations structure to update
        :type data: dict
        """
        image_id = self._image_lookup[item.image_name]
        absolute = item.get_absolute()
        for obj in absolute:
            label = get_object_label(obj)
            if label not in self._category_lookup:
                if self.error_on_new_category:
                    raise Exception("Undefined label encountered with image %s: %s" % (item.image_name, label))
                self._category_lookup[label] = len(self._category_lookup) + 1
            category_id = self._category_lookup[label]
            annotation_id = len(data["annotations"]) + 1
            annotation = dict()
            annotation["id"] = annotation_id
            annotation["image_id"] = image_id
            annotation["category_id"] = category_id
            annotation["area"] = float(item.image_width * item.image_height)
            annotation["bbox"] = [obj.x, obj.y, obj.width, obj.height]
            annotation["iscrowd"] = 0
            if obj.has_polygon():
                x_list = obj.get_polygon_x()
                y_list = obj.get_polygon_y()
            else:
                x_list = [obj.x, obj.x + obj.width - 1, obj.x + obj.width - 1, obj.x]
                y_list = [obj.y, obj.y, obj.y + obj.height - 1, obj.y + obj.height - 1]
            segmentation = []
            for x, y in zip(x_list, y_list):
                segmentation.append(x)
                segmentation.append(y)
            annotation["segmentation"] = [segmentation]
            data["annotations"].append(annotation)

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        for item in data:
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            # write image
            path = os.path.join(sub_dir, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # append annotations
            if sub_dir not in self._splits:
                self._splits[sub_dir] = self._init_annotations()
            self._append_image(self._splits[sub_dir], item)
            if item.has_annotation():
                self._append_annotations(self._splits[sub_dir], item)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        for sub_dir, annotations in self._splits.items():
            # save annotations
            annotations["categories"] = self._create_categories()
            path = os.path.join(sub_dir, "annotations.json")
            self.logger().info("Writing annotations to: %s" % path)
            with open(path, "w") as fp:
                json.dump(annotations, fp)

            # save categories
            if self.category_output_file is not None:
                categories = self._category_lookup.keys()
                if self.sort_categories:
                    categories = sorted(categories)
                path = os.path.join(sub_dir, self.category_output_file)
                self.logger().info("Writing categories to: %s" % path)
                with open(path, "w") as fp:
                    fp.write(",".join(categories))
