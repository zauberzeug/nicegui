from collections.abc import Callable
from typing import Any

_converters: dict[type, Callable[[Any], Any]] = {}


def register_type(cls: type, converter: Callable[[Any], Any]) -> None:
    """Register a converter for serializing objects of a custom type to JSON.

    The converter is applied to instances of `cls` and its subclasses and must return a JSON-serializable value,
    like a dict or a string.
    The first matching registration wins, so register more specific types before their base classes.
    Types which are supported natively by the JSON serializer, like dataclasses or datetimes, cannot be overridden.

    :param cls: the type to convert
    :param converter: function that converts an object of this type into a JSON-serializable value
    """
    _converters[cls] = converter


def find_converter(obj: Any) -> Callable[[Any], Any] | None:
    """Return the registered converter for the given object, or ``None`` if there is none."""
    for cls, converter in _converters.items():
        if isinstance(obj, cls):
            return converter
    return None
