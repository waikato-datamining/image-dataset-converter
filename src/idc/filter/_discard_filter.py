import abc

from wai.logging import LOGGING_WARNING

from seppl.io import BatchFilter


class DiscardFilter(BatchFilter, abc.ABC):
    """
    Ancestor for filters that discard images.
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
        self.kept = 0
        self.discarded = 0

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self.kept = 0
        self.discarded = 0

    def _keep(self, item):
        """
        Increments the "kept" counter.

        :param item: the item that is kept
        """
        self.kept += 1

    def _discard(self, item):
        """
        Increments the "discarded" counter and logs the item that was discarded.

        :param item: the item that is discarded
        """
        self.discarded += 1
        self.logger().info("Discarding: %s" % str(item))

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.logger().info("# kept: %d" % self.kept)
        self.logger().info("# discarded: %d" % self.discarded)
