from typing import Callable, Optional

from fastapi import Request, Response

from ..element import Element
from ..events import UploadEventArguments, handle_event
from ..nicegui import app


class Upload(Element):

    def __init__(self, *,
                 multiple: bool = False,
                 on_upload: Optional[Callable] = None,
                 label: str = '',
                 auto_upload: bool = False,
                 ) -> None:
        """File Upload

        Based on Quasar's `QUploader <https://quasar.dev/vue-components/uploader>`_ component.

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param on_upload: callback to execute for each uploaded file (type: nicegui.events.UploadEventArguments)
        :param label: label for the uploader (default: `''`)
        :param auto_upload: automatically upload files when they are selected (default: `False`)
        """
        super().__init__('q-uploader')
        self._props['multiple'] = multiple
        self._props['label'] = label
        self._props['auto-upload'] = auto_upload
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'

        @app.post(self._props['url'])
        async def upload_route(request: Request) -> Response:
            for data in (await request.form()).values():
                args = UploadEventArguments(
                    sender=self,
                    client=self.client,
                    content=data.file,
                    name=data.filename,
                    type=data.content_type,
                )
                handle_event(on_upload, args)
            return {'upload': 'success'}

    def reset(self) -> None:
        self.run_method('reset')

    def delete(self) -> None:
        app.remove_route(self._props['url'])
        super().delete()
