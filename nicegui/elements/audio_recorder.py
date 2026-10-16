from typing import cast

from fastapi import Request
from starlette.datastructures import UploadFile
from typing_extensions import Self

from .. import core
from ..element import Element
from ..events import GenericEventArguments, Handler, UploadEventArguments, handle_event
from ..nicegui import app
from .upload_files import create_file_upload


class AudioRecorder(Element, component='audio_recorder.js'):

    def __init__(self, *,
                 mime_type: str | None = None,
                 on_audio_ready: Handler[UploadEventArguments] | None = None,
                 on_error: Handler[GenericEventArguments] | None = None,
                 ) -> None:
        """Audio Recorder

        Records audio from the user's microphone using the browser's
        `MediaRecorder API <https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder>`_.
        The element itself is invisible; call ``start()`` and ``stop()``, e.g. from buttons.
        The browser asks for microphone permission on the first ``start()``.

        When a recording is stopped, it is uploaded to the server and ``on_audio_ready`` is called
        with an ``UploadEventArguments`` object whose ``file`` attribute holds the recording.
        If the microphone cannot be accessed (e.g. because the user denied the permission, ``name`` is "NotAllowedError")
        or the upload fails (``name`` is "UploadError"), ``on_error`` is called with ``name`` and ``message`` in ``e.args``.

        :param mime_type: preferred MIME type like "audio/webm" (default: `None`, i.e. the browser's choice)
        :param on_audio_ready: callback to execute when a recording is available
        :param on_error: callback to execute when recording or uploading fails
        """
        super().__init__()
        self._props.set_optional('mime_type', mime_type)
        self._registered_url = f'/_nicegui/client/{self.client.id}/audio_recorder/{self.id}'
        self._props['url'] = self._registered_url
        self._audio_ready_handlers = [on_audio_ready] if on_audio_ready else []

        @app.post(self._registered_url, include_in_schema=core.app.config.endpoint_documentation in {'internal', 'all'})
        async def upload_route(request: Request) -> dict[str, str]:
            async with request.form() as form:
                file = await create_file_upload(cast(UploadFile, form['file']))
            for handler in self._audio_ready_handlers:
                handle_event(handler, UploadEventArguments(sender=self, client=self.client, file=file))
            return {'upload': 'success'}

        if on_error:
            self.on_error(on_error)

    def on_audio_ready(self, callback: Handler[UploadEventArguments]) -> Self:
        """Add a callback to be invoked when a recording is available."""
        self._audio_ready_handlers.append(callback)
        return self

    def on_error(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when recording or uploading fails."""
        self.on('error', callback)
        return self

    def start(self) -> None:
        """Start recording."""
        self.run_method('start')

    def stop(self) -> None:
        """Stop recording and upload the audio."""
        self.run_method('stop')

    def _handle_delete(self) -> None:
        app.remove_route(self._registered_url)
        super()._handle_delete()
