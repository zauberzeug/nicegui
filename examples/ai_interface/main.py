#!/usr/bin/env python3
import base64
import io

import replicate  # very nice API to run AI models; see https://replicate.com/

from nicegui import run, ui
from nicegui.events import UploadEventArguments


async def transcribe(e: UploadEventArguments):
    transcription.text = 'Transcribing...'
    prediction = await run.io_bound(
        replicate.run,
        'openai/whisper:8099696689d249cf8b122d833c36ac3f75505c666a395ca40ef26f68e7d3d16e',
        input={'audio': io.BytesIO(await e.file.read())},
    )
    text = prediction.get('text') or prediction.get('transcription') or 'no transcription'
    transcription.set_text(f'result: "{text}"')


async def generate_image():
    image.source = 'https://dummyimage.com/600x400/ccc/000000.png&text=building+image...'
    prediction = await run.io_bound(
        replicate.run,
        'stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
        input={'prompt': prompt.value},
    )
    output = prediction[0] if isinstance(prediction, (list, tuple)) else prediction
    if hasattr(output, 'read'):
        data = output.read()
        mime = getattr(output, 'mime_type', None) or getattr(output, 'content_type', None) or 'image/webp'
        b64 = base64.b64encode(data).decode('ascii')
        image.source = f'data:{mime};base64,{b64}'
    elif hasattr(output, 'url'):
        image.source = output.url
    else:
        image.source = str(output)

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
