import re


def kebab_to_camel_case(string: str) -> str:
    """Convert a kebab-case string to camelCase."""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))


def camel_to_title_case(string: str) -> str:
    """Convert a camelCase string to Title Case."""
    return ' '.join(word[:1].upper() + word[1:]
                    for word in re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split())


def event_type_to_camel_case(string: str) -> str:
    """Convert an event type string to camelCase, leaving modifiers and keys after the first '.' untouched."""
    event_name, *modifiers = string.split('.')
    return '.'.join([kebab_to_camel_case(event_name), *modifiers])


def remove_indentation(text: str) -> str:
    """Remove indentation from a multi-line string based on the indentation of the first non-empty line."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    indentation = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join(line[indentation:] for line in lines)
