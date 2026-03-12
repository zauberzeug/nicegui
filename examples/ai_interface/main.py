#!/usr/bin/env python3
import io
import os

import replicate  # very nice API to run AI models; see https://replicate.com/

from nicegui import events, run, ui

os.environ['REPLICATE_API_TOKEN'] = '...'  # TODO: set your Replicate API token here


async def transcribe_audio(e: events.UploadEventArguments):
    transcription.text = 'Transcribing...'
    output = await run.io_bound(
        replicate.run,
        'openai/whisper:8099696689d249cf8b122d833c36ac3f75505c666a395ca40ef26f68e7d3d16e',
        input={'audio': io.BytesIO(await e.file.read())},
    )
    transcription.text = output.get('transcription', 'Transcription failed.')


async def generate_image():
    image_button.props('loading')
    output = await run.io_bound(
        replicate.run,
        'stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
        input={'prompt': prompt.value},
    )
    image_button.props(remove='loading')
    images.clear()
    for image in output:
        ui.image(image.url).classes('w-100 border border-gray-300 rounded-md')

with ui.row().classes('gap-16'):
    with ui.column().classes('w-100 items-stretch'):
        ui.label('OpenAI Whisper (voice transcription)').classes('text-2xl')
        ui.upload(on_upload=transcribe_audio, auto_upload=True)
        transcription = ui.label().classes('text-xl')
    with ui.column().classes('w-100 items-stretch'):
        ui.label('Stable Diffusion (image generator)').classes('text-2xl')
        prompt = ui.input('Your prompt').on('keydown.enter', generate_image)
        image_button = ui.button('Generate image', on_click=generate_image)
        images = ui.column()

ui.run()
