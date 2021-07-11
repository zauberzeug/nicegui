import justpy as jp
from typing import Callable
import base64
from .element import Element
from ..utils import handle_exceptions

class Upload(Element):

    def __init__(self,
                 *,
                 multiple: bool = False,
                 on_upload: Callable = None,
                 ):
        """File Upload Element

        :param multiple: allow uploading multiple files at once (default: False)
        :param on_upload: callback to execute when a file is uploaded (list of bytearrays)
        """
        self.on_upload = handle_exceptions(on_upload)
        view = jp.Form(enctype='multipart/form-data', classes='flex gap-4 items-center',
                       submit=lambda s, m: self.submit(s, m))
        jp.Input(type='file', multiple=multiple, a=view)
        jp.QButton(type='submit', text='Upload', color='primary', a=view)

        super().__init__(view)

    def submit(self, _, msg):

        for form_data in msg.form_data:
            if form_data.type == 'file':
                self.on_upload([base64.b64decode(f.file_content) for f in form_data.files])
