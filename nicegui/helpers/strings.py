def kebab_to_camel_case(string: str) -> str:
    """Convert a kebab-case string to camelCase."""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))


def event_type_to_camel_case(string: str) -> str:
    """Convert an event type string to camelCase."""
    return '.'.join(kebab_to_camel_case(part) if part != '-' else part for part in string.split('.'))
