

import re
import isort


import inspect
from typing import Callable

UNCOMMENT_PATTERN = re.compile(r'^(\s*)# ?')


def _uncomment(text: str) -> str:
    return UNCOMMENT_PATTERN.sub(r'\1', text)  # NOTE: non-executed lines should be shown in the code examples


def get_full_code(f: Callable) -> str:
    """Get the full code of a function as a string."""
    if True:
        code = inspect.getsource(f).split('# END OF DEMO', 1)[0].strip().splitlines()
        code = [line for line in code if not line.endswith('# HIDE')]
        while not code[0].strip().startswith(('def', 'async def')):
            del code[0]
        del code[0]
        if code[0].strip().startswith('"""'):
            while code[0].strip() != '"""':
                del code[0]
            del code[0]
        indentation = len(code[0]) - len(code[0].lstrip())
        code = [line[indentation:] for line in code]
        code = ['from nicegui import ui'] + [_uncomment(line) for line in code]
        code = ['' if line == '#' else line for line in code]
        if not code[-1].startswith('ui.run('):
            code.append('')
            code.append('ui.run()')
        full_code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
        return full_code
