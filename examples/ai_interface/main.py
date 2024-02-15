#!/usr/bin/env python3
import io

import replicate  # very nice API to run AI models; see https://replicate.com/

from nicegui import run, ui
from nicegui.events import UploadEventArguments


async def transcribe(e: UploadEventArguments):
    """
    Transcribes the audio content provided in the UploadEventArguments object.

    Args:
        e (UploadEventArguments): The event arguments containing the uploaded audio content.

    Returns:
        None

    Raises:
        None

    Usage:
        1. Call this function passing the UploadEventArguments object as the argument.
        2. The function will set the 'transcription' text to 'Transcribing...' to indicate the transcription process has started.
        3. It retrieves the model and version for transcription from the replicate.models dictionary.
        4. The function uses the 'predict' method of the version object to transcribe the audio content.
        5. The transcribed text is extracted from the prediction result.
        6. The 'transcription' text is updated with the transcribed result.
    """
    transcription.text = 'Transcribing...'
    model = replicate.models.get('openai/whisper')
    version = model.versions.get('30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed')
    prediction = await run.io_bound(version.predict, audio=io.BytesIO(e.content.read()))
    text = prediction.get('transcription', 'no transcription')
    transcription.set_text(f'result: "{text}"')


async def generate_image():
    """
    Generates an image using a pre-trained AI model.

    This function sets the source of an image widget to a generated image using a pre-trained AI model.
    It follows the following steps:
    1. Sets the source of the image widget to a placeholder image.
    2. Retrieves the pre-trained AI model named 'stability-ai/stable-diffusion'.
    3. Retrieves a specific version of the model using the version ID 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf'.
    4. Calls the 'predict' method of the model's version, passing the value of the 'prompt' variable.
    5. Sets the source of the image widget to the generated image returned by the 'predict' method.

    Note: This function assumes the existence of the following variables:
    - 'image': An image widget to display the generated image.
    - 'prompt': A variable containing the prompt for the AI model.

    Usage:
    1. Ensure that the 'image' and 'prompt' variables are properly defined.
    2. Call the 'generate_image' function to generate and display the image.

    Example:
    ```
    image = ImageWidget()
    prompt = "Generate a beautiful landscape"
    await generate_image()
    ```

    """
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
