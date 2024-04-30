from .. import json
from .javascript import run_javascript


async def read() -> str:
    """Read text from the clipboard."""
    return await run_javascript('navigator.clipboard.readText()')


def write(text: str) -> None:
    """Write text to the clipboard.

    :param text: text to write
    """
    run_javascript(f'navigator.clipboard.writeText({json.dumps(text)})')
