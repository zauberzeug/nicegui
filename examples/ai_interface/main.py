#!/usr/bin/env python3

import asyncio
import functools
import io
from typing import Callable

import replicate
from nicegui import ui
from nicegui.events import UploadEventArguments


async def io_bound(callback: Callable, *args: any, **kwargs: any):
    return await asyncio.get_event_loop().run_in_executor(None, functools.partial(callback, *args, **kwargs))


async def transcribe(upload: UploadEventArguments):
    transcription.text = 'Transcribing...'
    model = replicate.models.get('openai/whisper')
    prediction = await io_bound(model.predict, audio=io.BytesIO(upload.files[0]))
    text = prediction.get("transcription", "no transcription")
    transcription.set_text(f'result: "{text}"')


ui.label('OpenAI Whisper (voice transcription)').classes('text-2xl')
ui.upload(on_upload=transcribe).style('width: 20em')
transcription = ui.label().classes('text-xl')

ui.run()
