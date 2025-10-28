import inspect
import re
from typing import Callable

import isort

UNCOMMENT_PATTERN = re.compile(r'^(\s*)# ?')


def _uncomment(text: str) -> str:
    return UNCOMMENT_PATTERN.sub(r'\1', text)  # NOTE: non-executed lines should be shown in the code examples


def get_full_code(f: Callable) -> str:
    """Get the full code of a function as a string."""
    code = inspect.getsource(f).split('# END OF DEMO', 1)[0].strip().splitlines()
    code = [line for line in code if not line.endswith('# HIDE')]
    while not code[0].strip().startswith(('def', 'async def')):
        del code[0]
    del code[0]
    if code[0].strip().startswith('"""'):
        while code[0].strip() != '"""':
            del code[0]
        del code[0]
    non_empty_lines = [line for line in code if line.strip()]
    indentation = len(non_empty_lines[0]) - len(non_empty_lines[0].lstrip())
    code = [line[indentation:] for line in code]
    has_root_function = any(line.strip().startswith('def root(') for line in code)
    code = ['from nicegui import ui'] + [_uncomment(line) for line in code]
    code = ['' if line == '#' else line for line in code]

    if has_root_function:
        code = [line for line in code if line.strip() != 'return root']

    if not code[-1].startswith('ui.run('):
        code.append('ui.run(root)' if has_root_function else 'ui.run()')

    code.insert(-1, '')  # ensure blank line before ui.run
    while code[-3] == '':
        code.pop(-3)  # avoid double blank line before ui.run

    return isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
