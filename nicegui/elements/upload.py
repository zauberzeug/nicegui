from typing import Any, Callable, Dict, Optional, cast

from fastapi import Request
from starlette.datastructures import UploadFile
from typing_extensions import Self

from ..events import MultiUploadEventArguments, UiEventArguments, UploadEventArguments, handle_event
from ..nicegui import app
from .mixins.disableable_element import DisableableElement


class Upload(DisableableElement, component='upload.js'):

    def __init__(self, *,
                 multiple: bool = False,
                 max_file_size: Optional[int] = None,
                 max_total_size: Optional[int] = None,
                 max_files: Optional[int] = None,
                 on_upload: Optional[Callable[..., Any]] = None,
                 on_multi_upload: Optional[Callable[..., Any]] = None,
                 on_rejected: Optional[Callable[..., Any]] = None,
                 label: str = '',
                 auto_upload: bool = False,
                 ) -> None:
        """File Upload

        Based on Quasar's `QUploader <https://quasar.dev/vue-components/uploader>`_ component.

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param max_file_size: maximum file size in bytes (default: `0`)
        :param max_total_size: maximum total size of all files in bytes (default: `0`)
        :param max_files: maximum number of files (default: `0`)
        :param on_upload: callback to execute for each uploaded file
        :param on_multi_upload: callback to execute after multiple files have been uploaded
        :param on_rejected: callback to execute for each rejected file
        :param label: label for the uploader (default: `''`)
        :param auto_upload: automatically upload files when they are selected (default: `False`)
        """
        super().__init__()
        self._props['multiple'] = multiple
        self._props['label'] = label
        self._props['auto-upload'] = auto_upload
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'

        if max_file_size is not None:
            self._props['max-file-size'] = max_file_size

        if max_total_size is not None:
            self._props['max-total-size'] = max_total_size

        if max_files is not None:
            self._props['max-files'] = max_files

        if multiple and on_multi_upload:
            self._props['batch'] = True

        self._upload_handlers = [on_upload] if on_upload else []
        self._multi_upload_handlers = [on_multi_upload] if on_multi_upload else []

        @app.post(self._props['url'])
        async def upload_route(request: Request) -> Dict[str, str]:
            form = await request.form()
            for data in form.values():
                for upload_handler in self._upload_handlers:
                    handle_event(upload_handler, UploadEventArguments(
                        sender=self,
                        client=self.client,
                        content=cast(UploadFile, data).file,
                        name=cast(UploadFile, data).filename or '',
                        type=cast(UploadFile, data).content_type or '',
                    ))
            for multi_upload_handler in self._multi_upload_handlers:
                handle_event(multi_upload_handler, MultiUploadEventArguments(
                    sender=self,
                    client=self.client,
                    contents=[cast(UploadFile, data).file for data in form.values()],
                    names=[cast(UploadFile, data).filename or '' for data in form.values()],
                    types=[cast(UploadFile, data).content_type or '' for data in form.values()],
                ))
            return {'upload': 'success'}

        if on_rejected:
            self.on_rejected(on_rejected)

    def on_upload(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when a file is uploaded."""
        self._upload_handlers.append(callback)
        return self

    def on_multi_upload(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when multiple files have been uploaded."""
        self._multi_upload_handlers.append(callback)
        return self

    def on_rejected(self, callback: Callable[..., Any]) -> Self:
        """Add a callback to be invoked when a file is rejected."""
        self.on('rejected', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
        return self

    def reset(self) -> None:
        """Clear the upload queue."""
        self.run_method('reset')

    def _handle_delete(self) -> None:
        app.remove_route(self._props['url'])
        super()._handle_delete()
