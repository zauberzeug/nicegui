from .. import json


def dumps(data: object, identifier: str, *, indent: bool = False) -> str:
    """Serialize for backup; on failure, raise with the identifier and the offending key path."""
    try:
        return json.dumps(data, indent=indent)
    except TypeError as e:
        if (leaf := _find_offending_leaf(data)) is None:
            raise TypeError(f'Could not serialize {identifier}: {e}') from e
        path, value = leaf
        type_name = 'set' if isinstance(value, set) else type(value).__name__
        raise TypeError(
            f'Could not serialize {identifier} at {path}: value of type {type_name!r} is not JSON-serializable'
        ) from e


def _find_offending_leaf(data: object) -> tuple[str, object] | None:
    items = data.items() if isinstance(data, dict) else enumerate(data) if isinstance(data, (list, tuple)) else ()
    for key, value in items:
        try:
            json.dumps(value)
        except TypeError:
            if (deeper := _find_offending_leaf(value)) is None:
                return f'[{key!r}]', value
            return f'[{key!r}]' + deeper[0], deeper[1]
    return None
