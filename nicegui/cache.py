import hashlib
from typing import Dict, List, Set, TypeVar, Union, overload

from . import json


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
def cache(x: List) -> CachedList: ...


@overload
def cache(x: Dict) -> CachedDict: ...


def cache(x):
    """Mark an object as cached by converting it to a cached subtype."""
    if isinstance(x, str):
        return CachedStr(x)
    if isinstance(x, list):
        return CachedList(x)
    if isinstance(x, dict):
        return CachedDict(x)
    raise ValueError(f'Unsupported type: {type(x)}')


T = TypeVar('T')


def add_hash(obj: T, known_hashes: Set[str]) -> Union[T, str]:
    """Serialize an object to a JSON-compatible format."""
    if isinstance(obj, Cached):
        serialized = json.dumps(obj)
        hash_id = hashlib.sha256(serialized.encode()).hexdigest()[:32]
        if hash_id in known_hashes:
            return f'CACHE_{hash_id}'
        else:
            known_hashes.add(hash_id)
            return f'CACHE_{hash_id}_{serialized}'
    else:
        return obj
