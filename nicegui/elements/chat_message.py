from typing import Callable, Optional

from fastapi import Request, Response

from ..dependencies import register_component
from ..events import EventArguments, UploadEventArguments, handle_event
from ..nicegui import app
from .mixins.disableable_element import DisableableElement

register_component('chat_message', __file__, 'chat_message.js')


class ChatMessage(DisableableElement):

    def __init__(self, *,
                 sent: Optional[bool] = False,
                 label: Optional[str] = '',
                 text: Optional[str] = '',
                 stamp: Optional[str] = '',
                 name: Optional[str] = None,
                 avatar: Optional[str] = None,
                 ) -> None:
        """Chat Message

        Based on Quasar's `QUploader <https://quasar.dev/vue-components/chat_xxxx>`_ component.

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param max_file_size: maximum file size in bytes (default: `0`)
        :param max_total_size: maximum total size of all files in bytes (default: `0`)
        :param max_files: maximum number of files (default: `0`)
        :param on_upload: callback to execute for each uploaded file (type: nicegui.events.UploadEventArguments)
        :param on_rejected: callback to execute for each rejected file
        :param label: label for the uploader (default: `''`)
        :param auto_upload: automatically upload files when they are selected (default: `False`)
        """
        super().__init__(tag='chat_message')
        self._props['sent'] = sent
        self._props['label'] = label
        self._props['text'] = text
        self._props['stamp'] = stamp
        self._props['name'] = name
        self._props['avatar'] = avatar
