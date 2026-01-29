from typing import cast

from fastapi import Request
from starlette.datastructures import UploadFile
from typing_extensions import Self

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import Handler, MultiUploadEventArguments, UiEventArguments, UploadEventArguments, handle_event
from ..nicegui import app
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .upload_files import create_file_upload


class Upload(LabelElement, DisableableElement, component='upload.js'):
    # pylint: disable=import-outside-toplevel
    from .upload_files import FileUpload, LargeFileUpload, SmallFileUpload

    @resolve_defaults
    def __init__(self, *,
                 multiple: bool = DEFAULT_PROP | False,
                 max_file_size: int | None = DEFAULT_PROP | None,
                 max_total_size: int | None = DEFAULT_PROP | None,
                 max_files: int | None = DEFAULT_PROP | None,
                 on_begin_upload: Handler[UiEventArguments] | None = None,
                 on_upload: Handler[UploadEventArguments] | None = None,
                 on_multi_upload: Handler[MultiUploadEventArguments] | None = None,
                 on_rejected: Handler[UiEventArguments] | None = None,
                 label: str = DEFAULT_PROP | '',
                 auto_upload: bool = DEFAULT_PROP | False,
                 ) -> None:
        """File Upload

        Based on Quasar's `QUploader <https://quasar.dev/vue-components/uploader>`_ component.

        Upload event handlers are called in the following order:

        1. ``on_begin_upload``: The client begins uploading one or more files to the server.
        2. ``on_upload``: The upload of an individual file is complete.
        3. ``on_multi_upload``: The upload of all selected files is complete.

        The following event handler is already called during the file selection process:

        - ``on_rejected``: One or more files have been rejected.

        :param multiple: allow uploading multiple files at once (default: `False`)
        :param max_file_size: maximum file size in bytes (default: `0`)
        :param max_total_size: maximum total size of all files in bytes (default: `0`)
        :param max_files: maximum number of files (default: `0`)
        :param on_begin_upload: callback to execute when upload begins  (*added in version 2.14.0*)
        :param on_upload: callback to execute for each uploaded file
        :param on_multi_upload: callback to execute after multiple files have been uploaded
        :param on_rejected: callback to execute when one or more files have been rejected during file selection
        :param label: label for the uploader (default: `''`)
        :param auto_upload: automatically upload files when they are selected (default: `False`)
        """
        super().__init__(label=label)
        self._props.set_bool('multiple', multiple)
        self._props.set_bool('auto-upload', auto_upload)
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'

        self._props.set_optional('max-file-size', max_file_size)
        self._props.set_optional('max-total-size', max_total_size)
        self._props.set_optional('max-files', max_files)

        if multiple and on_multi_upload:
            self._props['batch'] = True

        self._begin_upload_handlers = [on_begin_upload] if on_begin_upload else []
        self._upload_handlers = [on_upload] if on_upload else []
        self._multi_upload_handlers = [on_multi_upload] if on_multi_upload else []

        @app.post(self._props['url'])
        async def upload_route(request: Request) -> dict[str, str]:
            for begin_upload_handler in self._begin_upload_handlers:
                handle_event(begin_upload_handler, UiEventArguments(sender=self, client=self.client))
            async with request.form() as form:
                files = [await create_file_upload(cast(UploadFile, data)) for data in form.values()]
            await self.handle_uploads(files)
            return {'upload': 'success'}

        if on_rejected:
            self.on_rejected(on_rejected)

    async def handle_uploads(self, files: list[FileUpload]) -> None:
        """Handle the uploaded files.

        This method is primarily intended for internal use and for simulating file uploads in tests.
        """
        assert all(isinstance(f, Upload.FileUpload) for f in files), \
            'since NiceGUI 3.0, uploads must be a list of FileUpload instances'
        for file in files:
            for upload_handler in self._upload_handlers:
                handle_event(upload_handler, UploadEventArguments(sender=self, client=self.client, file=file))
        multi_upload_args = MultiUploadEventArguments(sender=self, client=self.client, files=files)
        for multi_upload_handler in self._multi_upload_handlers:
            handle_event(multi_upload_handler, multi_upload_args)

    def on_begin_upload(self, callback: Handler[UiEventArguments]) -> Self:
        """Add a callback to be invoked when the upload begins."""
        self._begin_upload_handlers.append(callback)
        return self

    def on_upload(self, callback: Handler[UploadEventArguments]) -> Self:
        """Add a callback to be invoked when a file is uploaded."""
        self._upload_handlers.append(callback)
        return self

    def on_multi_upload(self, callback: Handler[MultiUploadEventArguments]) -> Self:
        """Add a callback to be invoked when multiple files have been uploaded."""
        self._multi_upload_handlers.append(callback)
        return self

    def on_rejected(self, callback: Handler[UiEventArguments]) -> Self:
        """Add a callback to be invoked when one or more files have been rejected during file selection."""
        self.on('rejected', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
        return self

    def reset(self) -> None:
        """Clear the upload queue."""
        self.run_method('reset')

    def _handle_delete(self) -> None:
        app.remove_route(self._props['url'])
        super()._handle_delete()
