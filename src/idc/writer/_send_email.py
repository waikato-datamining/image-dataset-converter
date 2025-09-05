from email.mime.multipart import MIMEMultipart

from idc.api import ImageData
from kasperl.writer import SendEmail as KSendEmail


class SendEmail(KSendEmail):

    def _attach_item(self, message: MIMEMultipart, item) -> bool:
        """
        Attaches the item to the message.

        :param message: the message to attach to
        :type message: MIMEMultipart
        :param item: the item to attach
        :return: whether data type has handled
        :rtype: bool
        """
        if isinstance(item, ImageData):
            self._attach_data(message, item.image_bytes, item.image_name,
                              mime_main="image", mime_sub=item.image_format.lower())
            return True
        else:
            return False
