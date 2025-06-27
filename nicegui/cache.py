from typing import overload


class Cached:
    """A base class for cached objects."""


class CachedStr(Cached, str):
    """A string that is marked as cached."""


class CachedList(Cached, list):
    """A list that is marked as cached."""


class CachedDict(Cached, dict):
    """A dict that is marked as cached."""


@overload
def cache(x: str) -> CachedStr: ...


@overload
def cache(x: list) -> CachedList: ...


@overload
def cache(x: dict) -> CachedDict: ...


def cache(x):
    """Mark an object as cached by converting it to a cached subtype."""
    if isinstance(x, str):
        return CachedStr(x)
    if isinstance(x, list):
        return CachedList(x)
    if isinstance(x, dict):
        return CachedDict(x)
    raise ValueError(f'Unsupported type: {type(x)}')


def is_cached(obj) -> bool:
    """Check if an object is marked as cached."""
    return isinstance(obj, Cached)
