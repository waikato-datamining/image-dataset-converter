from typing import List

from wai.logging import LOGGING_WARNING

from idc.api import array_to_image, apply_exif_rotation, IDC_EXIF_AUTOROTATE, exif_autorotate, load_image_from_file
from kasperl.api import make_list, flatten_list, safe_deepcopy
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
        return "Automatically rotates the image according to the EXIF information (if applicable). May not work as expected if auto-rotation is enforced via environment variable " + IDC_EXIF_AUTOROTATE + " as the implicit rotation will lose the EXIF information."

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
        if exif_autorotate():
            self.logger().warning("EXIF auto-rotation is enforced via environment variable already " + IDC_EXIF_AUTOROTATE + "!")

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        implicit = exif_autorotate()

        for item in make_list(data):
            modified = False
            img_new = None
            if implicit:
                if item.source is not None:
                    img_new = load_image_from_file(item.source, autorotate=True)
                    modified = True
                else:
                    self.logger().warning("Implicit EXIF auto-rotation is enabled and no file name available, cannot apply EXIF rotation!")
            else:
                img = item.image
                img_new, modified = apply_exif_rotation(img)
            if modified:
                self.logger().info("Applied EXIF rotation: %s" % item.image_name)
                item_new = type(item)(source=None, image_name=item.image_name,
                                      data=array_to_image(img_new, item.image_format)[1].getvalue(),
                                      image=img_new, image_format=item.image_format,
                                      metadata=safe_deepcopy(item.get_metadata()),
                                      annotation=safe_deepcopy(item.annotation))
                self.rotated += 1
                result.append(item_new)
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
