from .. import json
from ..logging import log
from .javascript import run_javascript


async def read() -> str:
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
    return result or ''


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
