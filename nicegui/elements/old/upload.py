import base64
import traceback
from typing import Callable, Optional

import justpy as jp

from ..events import UploadEventArguments, handle_event
from .element import Element


class Upload(Element):

    def __init__(self, *,
                 multiple: bool = False,
                 on_upload: Optional[Callable] = None,
                 upload_button_text: str = 'Upload') -> None:
        """File Upload

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param on_upload: callback to execute when a file is uploaded (list of bytearrays)
        :param upload_button_text: text for the upload button
        """
        self.upload_handler = on_upload
        view = jp.Form(
            enctype='multipart/form-data',
            classes='flex gap-4 items-center',
            submit=lambda sender, msg: self.submit(sender, msg),
            temp=False,
        )
        jp.Input(type='file', multiple=multiple, change=lambda *_: False, a=view, temp=False)
        jp.QBtn(type='submit', text=upload_button_text, color='primary', a=view, temp=False)

        super().__init__(view)

    def submit(self, _, msg) -> Optional[bool]:
        try:
            page_update = False
            for form_data in msg.form_data:
                if form_data.type == 'file':
                    files = [base64.b64decode(f.file_content) for f in form_data.files]
                    names = [f.name for f in form_data.files]
                    arguments = UploadEventArguments(sender=self, socket=msg.websocket, files=files, names=names)
                    if handle_event(self.upload_handler, arguments):
                        page_update = None
            return page_update
        except Exception:
            traceback.print_exc()
