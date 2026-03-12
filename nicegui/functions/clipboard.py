from __future__ import annotations

import io
from contextlib import suppress

from .. import json, optional_features
from ..logging import log
from .javascript import run_javascript

with suppress(ImportError):
    from PIL import Image as PIL_Image
    optional_features.register('pillow')


async def read() -> str | None:
    """Read text from the clipboard.

    Note: This function only works in secure contexts (HTTPS or localhost).
    """
    result = await run_javascript('''
        if (navigator.clipboard) {
            return navigator.clipboard.readText()
        }
        else {
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).')
        }
    ''')
    if result is None:
        log.warning('Clipboard API is only available in secure contexts (HTTPS or localhost).')
    return result


def write(text: str) -> None:
    """Write text to the clipboard.

    Note: This function only works in secure contexts (HTTPS or localhost).

    :param text: text to write
    """
    run_javascript(f'''
        if (navigator.clipboard) {{
            navigator.clipboard.writeText({json.dumps(text)})
        }}
        else {{
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).')
        }}
    ''')


async def read_image() -> PIL_Image.Image | None:
    """Read PIL images from the clipboard.

    Note: This function only works in secure contexts (HTTPS or localhost) and requires Pillow to be installed.

    *Added in version 2.10.0*
    """
    if not optional_features.has('pillow'):
        log.warning('Pillow is not installed, so we cannot read images from the clipboard.')
        return None
    content = await run_javascript('''
        if (navigator.clipboard) {
            const items = await navigator.clipboard.read();
            for (const item of items) {
                if (item.types.length > 0 && /^image/.test(item.types[0])) {
                    return await item.getType(item.types[0]);
                }
            }
        }
        else {
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).');
        }
    ''', timeout=5)
    if not content:
        return None
    buffer = io.BytesIO(content)
    return PIL_Image.open(buffer)
