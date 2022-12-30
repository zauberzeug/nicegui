from typing import Callable, Dict, Optional

from ..dependencies import register_component
from ..element import Element
from ..events import UploadEventArguments, UploadFile, handle_event

register_component('upload', __file__, 'upload.vue')


class Upload(Element):

    def __init__(self, *,
                 multiple: bool = False,
                 on_upload: Optional[Callable] = None,
                 file_picker_label: str = '',
                 upload_button_icon: str = 'file_upload') -> None:
        """File Upload

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param on_upload: callback to execute when a file is uploaded (list of bytearrays)
        :param file_picker_label: label for the file picker element
        :param upload_button_icon: icon for the upload button
        """
        super().__init__('upload')
        self.classes('row items-center gap-2')
        self._props['multiple'] = multiple
        self._props['file_picker_label'] = file_picker_label
        self._props['upload_button_icon'] = upload_button_icon

        def upload(msg: Dict) -> None:
            files = [
                UploadFile(
                    content=file['content'],
                    name=file['name'],
                    lastModified=file['lastModified'],
                    size=file['size'],
                    type=file['type'],
                )
                for file in msg['args']
            ]
            handle_event(on_upload, UploadEventArguments(sender=self, client=self.client, files=files))
        self.on('upload', upload)

    def reset(self) -> None:
        self.run_method('reset')
