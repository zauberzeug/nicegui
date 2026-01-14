from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from .dataclasses import KWONLY_SLOTS
from .element import Element

T = TypeVar('T')

P = ParamSpec('P')
R = TypeVar('R')


@dataclass(**KWONLY_SLOTS)
class Sentinel:
    key: str | None
    source: str | None = None

    def __or__(self, other: T) -> T:
        return SentinelValue(key=self.key, default=other, source=self.source)  # type: ignore[return-value]


@dataclass(**KWONLY_SLOTS)
class SentinelValue:
    key: str | None
    default: Any
    source: str | None = None


class SentinelFactory:

    def __getitem__(self, prop_key: str) -> Sentinel:
        return Sentinel(key=prop_key)


def default(other: T) -> T:
    """For `DEFAULTS | ...` parameters, this marks a parameter input as a default.
    It will be applied automatically for subsequent elements."""
    return SentinelValue(key=None, default=other, source='default-marker')  # type: ignore[return-value]


DEFAULT_PROPS = SentinelFactory()
DEFAULT_PROP = Sentinel(key=None)
DEFAULTS = Sentinel(key=None, source='defaults')


def resolve_defaults(original_func: Callable[P, R]) -> Callable[P, R]:
    """This decorator makes the function resolve default properties set via ``default_props``.

    ^^^^^^^^^^^^^^^^^^^^^^^^^
    From ``.default_props()``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    If a parameter has a default value which looks like ``DEFAULT_PROPS['prop-key'] | default_value``,
    the actual value will be taken from the element's ``_default_props`` dictionary with key "prop-key" if present,
    otherwise the specified ``default_value`` is used.

    If a parameter has a default value which looks like ``DEFAULT_PROP | default_value``,
    the dictionary key will be inferred from the parameter name (converting snake_case to kebab-case).

    ^^^^^^^^^^^^^^^^^^^^^^^^^
    From ``ui.default()``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    If a parameter has a default value which looks like ``DEFAULTS | default_value``,
    the actual value will be taken from the element's ``_defaults`` dictionary if present,
    otherwise the specified ``default_value`` is used.

    If the input parameter value is marked with ``ui.default()``,
    the value will be set in the element's ``_defaults`` dictionary for subsequent elements.
    """
    signature = inspect.signature(original_func)

    @functools.wraps(original_func)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> R:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        el: Element = bound.arguments['self']

        for param_name, value in bound.arguments.items():
            if isinstance(value, SentinelValue):
                if value.source == 'default-marker':
                    kwargs[param_name] = value.default
                    el._defaults[param_name] = value.default  # pylint: disable=protected-access
                elif value.source == 'defaults':
                    kwargs[param_name] = el._defaults.get(param_name, value.default)  # pylint: disable=protected-access
                else:
                    key = value.key or param_name.replace('_', '-')
                    kwargs[param_name] = el._default_props.get(key, value.default)  # pylint: disable=protected-access
        return original_func(*args, **kwargs)

    return decorated
