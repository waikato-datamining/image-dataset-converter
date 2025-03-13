import argparse
import os
from datetime import datetime
from typing import List

from wai.logging import LOGGING_WARNING
from idc.api import ObjectDetectionData, SplittableStreamWriter, get_object_label, make_list, AnnotationsOnlyWriter, add_annotations_only_param
from opex import ObjectPredictions, ObjectPrediction, BBox, Polygon
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class OPEXObjectDetectionWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
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
        self.annotations_only = annotations_only

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-opex-od"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the bounding box/polygon definitions in OPEX .json format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.json files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
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

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            absolute = None
            if item.has_annotation():
                absolute = item.get_absolute()

            # image
            path = sub_dir
            os.makedirs(path, exist_ok=True)
            path = os.path.join(path, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            # annotations
            if absolute is not None:
                objs = []
                for obj in absolute:
                    # score
                    score = 0.0
                    if "score" in obj.metadata:
                        try:
                            score = float(obj.metadata["score"])
                        except:
                            pass
                    # label
                    label = get_object_label(obj)
                    # meta data
                    meta = dict()
                    for k, v in obj.metadata.items():
                        if k in ["score", "type"]:
                            continue
                        meta[k] = str(v)
                    if len(meta) == 0:
                        meta = None
                    # bbox
                    bbox = BBox(left=obj.x, top=obj.y, right=obj.x + obj.width - 1, bottom=obj.y + obj.height - 1)
                    # polygon
                    points = []
                    if obj.has_polygon():
                        for x, y in zip(obj.get_polygon_x(), obj.get_polygon_y()):
                            points.append([x, y])
                    else:
                        points.append([obj.x, obj.y])
                        points.append([obj.x + obj.width - 1, obj.y])
                        points.append([obj.x + obj.width - 1, obj.y + obj.height - 1])
                        points.append([obj.x, obj.y + obj.height - 1])
                    polygon = Polygon(points=points)
                    objs.append(ObjectPrediction(score=score, label=label, bbox=bbox, polygon=polygon, meta=meta))

                # meta
                meta = dict()
                if item.has_metadata():
                    for k, v in item.get_metadata().items():
                        if k.startswith("Parent ID["):
                            continue
                        meta[k] = str(v)
                if len(meta) == 0:
                    meta = None

                # timestamp
                ts = datetime.now().strftime("%Y%m%d_%H%M%S.%f")

                # ID
                if item.image_name is None:
                    id = ts
                else:
                    id = os.path.splitext(os.path.basename(item.image_name))[0]

                # assemble predictions
                if meta is None:
                    preds = ObjectPredictions(id=id, timestamp=ts, objects=objs)
                else:
                    preds = ObjectPredictions(id=id, timestamp=ts, objects=objs, meta=meta)

                path = sub_dir
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, item.image_name)
                path = os.path.splitext(path)[0] + ".json"
                self.logger().info("Writing annotations to: %s" % path)
                preds.save_json_to_file(path)
