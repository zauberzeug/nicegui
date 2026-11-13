"""Serve the photos used in documentation demos and examples, cropped to any size like picsum.photos did.

Most photos are from Unsplash (https://unsplash.com/license).
Their sources are listed in SOURCES.
Photos with unknown Unsplash source were reconstructed from archived picsum.photos crops in the Wayback Machine.
"""
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageOps

from nicegui import app

PATH = Path(__file__).parent / 'demo_images'
MAX_SIZE = 1280

SOURCES = {
    'bench': 'https://unsplash.com/photos/eG3k60PrTGY',
    'birds': 'picsum.photos/id/565 (Unsplash source unknown)',
    'bridge': 'https://unsplash.com/photos/nrLtvA05jk8',
    'drops': 'https://unsplash.com/photos/fTKetYpEKNQ',
    'feet': 'https://unsplash.com/photos/7Vz3DtQDT3Q',
    'grapes': 'picsum.photos/id/674 (Unsplash source unknown)',
    'hikers': 'picsum.photos/id/684 (Unsplash source unknown)',
    'mug': 'https://unsplash.com/photos/aeVA-j1y2BY',
    'night': 'https://unsplash.com/photos/8WClaa1CmZ0',
    'sea': 'https://unsplash.com/photos/OODWPtfXAF0',
    'valley': 'https://unsplash.com/photos/V0yAek6BgGk',
}

# mounted as a sub-application so that the website's default rate limits do not apply to image requests
images_app = FastAPI()


@images_app.get('/{name}/{width}/{height}')
def _image(name: str, width: int, height: int) -> Response:
    if name not in SOURCES:
        raise HTTPException(404, f'Unknown image "{name}"')
    if not 0 < width <= MAX_SIZE or not 0 < height <= MAX_SIZE:
        raise HTTPException(400, f'Width and height must be between 1 and {MAX_SIZE}')
    return Response(_crop(name, width, height), media_type='image/jpeg',
                    headers={'Cache-Control': 'public, max-age=86400'})


@lru_cache(maxsize=256)
def _crop(name: str, width: int, height: int) -> bytes:
    with Image.open(PATH / f'{name}.jpg') as image:
        cropped = ImageOps.fit(image, (width, height), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    cropped.save(buffer, format='JPEG', quality=85)
    return buffer.getvalue()


def setup() -> None:
    """Serve the demo images at /images/{name}/{width}/{height}."""
    app.mount('/images', images_app)
