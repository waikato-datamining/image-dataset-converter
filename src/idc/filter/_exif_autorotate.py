from typing import List

from PIL import ExifTags, ImageOps
from wai.logging import LOGGING_WARNING

from idc.api import image_to_bytesio
from kasperl.api import make_list, flatten_list
from seppl import AnyData
from seppl.io import BatchFilter


class ExifAutorotate(BatchFilter):
    """
    Automatically rotates the image according to the EXIF information (if applicable).
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.unmodified = 0
        self.rotated = 0

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "exif-autorotate"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Automatically rotates the image according to the EXIF information (if applicable)."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self.unmodified = 0
        self.rotated = 0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            img = item.image
            exif = img.getexif()
            modified = False
            for key, val in exif.items():
                if (key in ExifTags.TAGS) and (ExifTags.TAGS[key] == "Orientation"):
                    if val != 1:
                        modified = True
                        self.logger().info("Applying EXIF rotation: %s" % item.image_name)
                        img_new = ImageOps.exif_transpose(img)
                        data_new = image_to_bytesio(img_new, item.image_format)
                        item_new = item.duplicate(force_no_source=True, image=img_new, data=data_new.getvalue())
                        result.append(item_new)
                    break

            if modified:
                self.rotated += 1
            else:
                self.logger().info("No need to rotate: %s" % item.image_name)
                self.unmodified += 1
                result.append(item)

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.logger().info("# rotated: %d" % self.rotated)
        self.logger().info("# unmodified: %d" % self.unmodified)
