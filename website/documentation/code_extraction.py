import inspect
import re
from typing import Callable

import isort

UNCOMMENT_PATTERN = re.compile(r'^(\s*)# ?')
TRANSFORM_COMMENT_PATTERN = re.compile(r'#\s*TRANSFORM:\s*.+')
SUBPAGES_PATTERN = re.compile(r'(\w+\s*=\s*)?ui\.sub_pages\(')
LINK_PATTERN = re.compile(r'\bui\.link\(')
TRANSFORM_VARNAME_PATTERN = re.compile(r'#\s*TRANSFORM:\s*(\w+)(?:\s+(.+))?$')


def _uncomment(text: str) -> str:
    return UNCOMMENT_PATTERN.sub(r'\1', text)  # NOTE: non-executed lines should be shown in the code examples


def get_full_code(f: Callable, *, keep_transform: bool = False) -> str:
    """Get the full code of a function as a string.

    Args:
        f: The function to extract code from
        keep_transform: If True, keep TRANSFORM comments (for transformation), else strip them (for display)
    """
    code = inspect.getsource(f).split('# END OF DEMO', 1)[0].strip().splitlines()
    if not keep_transform:
        code = [TRANSFORM_COMMENT_PATTERN.sub('', line).rstrip() for line in code]
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
    if not keep_transform:
        code = [_uncomment(line) for line in code]
    code = ['from nicegui import ui', *code]
    code = ['' if line == '#' else line for line in code]

    if any(line.strip().startswith('def root(') for line in code):
        code.append('')
        code.append('ui.run(root)')
    elif not code[-1].startswith('ui.run('):
        code.append('')
        code.append('ui.run()')
    full_code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
    return full_code


def _process_subpages_call(subpages_call_lines: list[str], sub_pages_var: str, indent: int) -> list[str]:
    """Process a complete ui.sub_pages() call and return transformed lines."""
    result_lines = []
    full_call = '\n'.join(subpages_call_lines)
    call_content = SUBPAGES_PATTERN.sub('', full_call, count=1)

    chained_methods = ''
    paren_depth = 0
    close_paren_idx = -1

    for i, char in enumerate(call_content):
        if char == '(':
            paren_depth += 1
        elif char == ')':
            if paren_depth == 0:
                close_paren_idx = i
                break
            paren_depth -= 1

    if close_paren_idx != -1:
        chained_methods = call_content[close_paren_idx + 1:].strip()
        call_content = call_content[:close_paren_idx].strip()
    else:
        call_content = call_content.rstrip().rstrip(')').rstrip()

    if not call_content or call_content.strip() == '':
        pass
    elif ', data=' in call_content or ',data=' in call_content:
        parts = call_content.rsplit(
            ', data=', 1) if ', data=' in call_content else call_content.rsplit(',data=', 1)
        routes_part = parts[0].strip()
        data_part = parts[1].strip()
        result_lines.append(' ' * indent + f'{sub_pages_var}.routes = {routes_part}')
        result_lines.append(' ' * indent + f'{sub_pages_var}.data = {data_part}')
    else:
        result_lines.append(' ' * indent + f'{sub_pages_var}.routes = {call_content.strip()}')

    if chained_methods:
        result_lines.append(' ' * indent + f'{sub_pages_var}{chained_methods}')

    result_lines.append(' ' * indent + f'{sub_pages_var}.init()')
    return result_lines


def transform_for_demo_execution(code: str) -> str:
    """Transform code for demo execution by replacing ui.sub_pages and ui.link with FakeSubPages equivalents."""
    lines = code.split('\n')
    lines = [line for line in lines if not line.strip().startswith('#')]
    lines = [line.removesuffix('  # HIDE').removesuffix(' # HIDE').removesuffix('# HIDE').rstrip() for line in lines]
    if not any('ui.sub_pages' in line for line in lines):
        return '\n'.join(lines)

    transformed_lines = []
    sub_pages_var_stack = []
    in_subpages_call = False
    paren_depth = 0
    current_sub_pages_var = None
    subpages_indent = 0
    subpages_call_lines = []
    instantiated_vars = set()

    for line in lines:
        varname_match = TRANSFORM_VARNAME_PATTERN.search(line)
        hint_var_name = None
        if varname_match:
            hint_var_name = varname_match.group(1)
            line = TRANSFORM_VARNAME_PATTERN.sub('', line).rstrip()  # noqa: PLW2901

        match = SUBPAGES_PATTERN.search(line)
        if match and not in_subpages_call:
            sub_pages_var = match.group(1).split('=')[0].strip() if match.group(1) else (hint_var_name or 'pages')

            if sub_pages_var not in sub_pages_var_stack:
                sub_pages_var_stack.append(sub_pages_var)

            if hint_var_name and sub_pages_var not in instantiated_vars and sub_pages_var != 'pages':
                subpages_indent = len(line) - len(line.lstrip())
                transformed_lines.append(' ' * subpages_indent + f'{sub_pages_var} = FakeSubPages()')
                instantiated_vars.add(sub_pages_var)

            subpages_indent = len(line) - len(line.lstrip())
            current_sub_pages_var = sub_pages_var
            in_subpages_call = True
            subpages_call_lines = [line]
            paren_depth = line.count('(') - line.count(')')

            if paren_depth == 0:
                transformed_lines.extend(_process_subpages_call(
                    subpages_call_lines, current_sub_pages_var, subpages_indent))
                in_subpages_call = False
                subpages_call_lines = []
        elif in_subpages_call:
            subpages_call_lines.append(line)
            paren_depth += line.count('(') - line.count(')')
            if paren_depth == 0:
                transformed_lines.extend(_process_subpages_call(
                    subpages_call_lines, current_sub_pages_var, subpages_indent))
                in_subpages_call = False
                subpages_call_lines = []
        elif 'ui.link(' in line:
            if varname_match:
                var_name = varname_match.group(1)
                if var_name not in instantiated_vars and var_name != 'pages':
                    indent = len(line) - len(line.lstrip())
                    transformed_lines.append(' ' * indent + f'{var_name} = FakeSubPages()')
                    instantiated_vars.add(var_name)
                if var_name not in sub_pages_var_stack:
                    sub_pages_var_stack.append(var_name)

                extra_args = varname_match.group(2)
                if extra_args:
                    link_match = re.match(r'(\s*)ui\.link\(([^,]+),', line)
                    if link_match:
                        indent = link_match.group(1)
                        text_arg = link_match.group(2)
                        transformed_lines.append(f'{indent}{var_name}.link({text_arg}, {extra_args})')
                    else:
                        transformed_lines.append(LINK_PATTERN.sub(f'{var_name}.link(', line))
                else:
                    transformed_lines.append(LINK_PATTERN.sub(f'{var_name}.link(', line))
            else:
                current_var = sub_pages_var_stack[0] if sub_pages_var_stack else 'pages'
                if not sub_pages_var_stack:
                    sub_pages_var_stack.append('pages')
                transformed_lines.append(LINK_PATTERN.sub(f'{current_var}.link(', line))
        else:
            transformed_lines.append(line)

    result = '\n'.join(transformed_lines)

    if sub_pages_var_stack:
        non_instantiated_vars = sorted(set(sub_pages_var_stack) - instantiated_vars)

        if non_instantiated_vars:
            sub_pages_init = '\n'.join(f'{var} = FakeSubPages()' for var in non_instantiated_vars)

            lines = result.split('\n')
            needs_fake_arguments = 'FakeArguments' in result
            imports = 'FakeArguments, FakeSubPages' if needs_fake_arguments else 'FakeSubPages'
            for i, line in enumerate(lines):
                if line.startswith('from nicegui import'):
                    lines.insert(
                        i + 1, f'from website.documentation.content.sub_pages_documentation import {imports}')
                    lines.insert(i + 2, '')
                    lines.insert(i + 3, sub_pages_init)
                    break
            result = '\n'.join(lines)
        else:
            lines = result.split('\n')
            needs_fake_arguments = 'FakeArguments' in result
            imports = 'FakeArguments, FakeSubPages' if needs_fake_arguments else 'FakeSubPages'
            for i, line in enumerate(lines):
                if line.startswith('from nicegui import'):
                    lines.insert(
                        i + 1, f'from website.documentation.content.sub_pages_documentation import {imports}')
                    break
            result = '\n'.join(lines)

    return result
