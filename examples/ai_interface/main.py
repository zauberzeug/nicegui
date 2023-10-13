#!/usr/bin/env python3
import io

import replicate  # very nice API to run AI models; see https://replicate.com/

from nicegui import run, ui
from nicegui.events import UploadEventArguments


async def transcribe(e: UploadEventArguments):
    transcription.text = 'Transcribing...'
    model = replicate.models.get('openai/whisper')
    version = model.versions.get('30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed')
    prediction = await run.io_bound(version.predict, audio=io.BytesIO(e.content.read()))
    text = prediction.get('transcription', 'no transcription')
    transcription.set_text(f'result: "{text}"')


async def generate_image():
    image.source = 'https://dummyimage.com/600x400/ccc/000000.png&text=building+image...'
    model = replicate.models.get('stability-ai/stable-diffusion')
    version = model.versions.get('db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf')
    prediction = await run.io_bound(version.predict, prompt=prompt.value)
    image.source = prediction[0]

# User Interface
with ui.row().style('gap:10em'):
    with ui.column():
        ui.label('OpenAI Whisper (voice transcription)').classes('text-2xl')
        ui.upload(on_upload=transcribe, auto_upload=True).style('width: 20em')
        transcription = ui.label().classes('text-xl')
    with ui.column():
        ui.label('Stable Diffusion (image generator)').classes('text-2xl')
        prompt = ui.input('prompt').style('width: 20em')
        ui.button('Generate', on_click=generate_image).style('width: 15em')
        image = ui.image().style('width: 60em')

ui.run()
