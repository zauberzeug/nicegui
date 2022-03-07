import traceback
import justpy as jp
from typing import Awaitable, Callable, Optional, Union
import base64

from ..events import UploadEventArguments, handle_event
from .element import Element

class Upload(Element):

    def __init__(self,
                 *,
                 multiple: bool = False,
                 on_upload: Optional[Union[Callable, Awaitable]] = None,
                 ):
        """File Upload Element

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param on_upload: callback to execute when a file is uploaded (list of bytearrays)
        """
        self.upload_handler = on_upload
        view = jp.Form(
            enctype='multipart/form-data',
            classes='flex gap-4 items-center',
            submit=lambda sender, msg: self.submit(sender, msg),
            temp=False,
        )
        jp.Input(type='file', multiple=multiple, a=view, temp=False)
        jp.QBtn(type='submit', text='Upload', color='primary', a=view, temp=False)

        super().__init__(view)

    def submit(self, _, msg):
        try:
            for form_data in msg.form_data:
                if form_data.type == 'file':
                    files = [base64.b64decode(f.file_content) for f in form_data.files]
                    arguments = UploadEventArguments(sender=self, files=files)
                    handle_event(self.upload_handler, arguments, update=self.parent_view)
        except Exception:
            traceback.print_exc()
