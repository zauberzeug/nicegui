from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from .element import Element

T = TypeVar('T')

P = ParamSpec('P')
R = TypeVar('R')


class Sentinel:

    def __init__(self, prop_key: str | None = None) -> None:
        self.key = prop_key
        self.default: Any

    def __or__(self, other: T) -> T:
        self.default = other
        return self  # type: ignore[return-value]


class SentinelFactory:

    def __getitem__(self, prop_key: str) -> Sentinel:
        return Sentinel(prop_key)


DEFAULT_PROPS = SentinelFactory()
DEFAULT_PROP = Sentinel()


def resolve_defaults(original_func: Callable[P, R]) -> Callable[P, R]:
    """This decorator makes the function resolve default properties set via ``default_props``.

    If a parameter has a default value which looks like ``DEFAULT_PROPS['prop-key'] | default_value``,
    the actual value will be taken from the element's ``_default_props`` dictionary with key "prop-key" if present,
    otherwise the specified ``default_value`` is used.

    If a parameter has a default value which looks like ``DEFAULT_PROP | default_value``,
    the dictionary key will be inferred from the parameter name (converting snake_case to kebab-case).
    """
    signature = inspect.signature(original_func)

    @functools.wraps(original_func)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> R:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        el: Element = bound.arguments['self']

        for param_name, value in bound.arguments.items():
            if isinstance(value, Sentinel):
                key = value.key or param_name.replace('_', '-')
                kwargs[param_name] = el._default_props.get(key, value.default)  # pylint: disable=protected-access
        return original_func(*args, **kwargs)

    return decorated
