import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ParamSpec, TypeVar, cast

from .element import Element

T = TypeVar('T')

P = ParamSpec('P')
R = TypeVar('R')


@dataclass(kw_only=True, slots=True)
class Sentinel:
    key: str | None

    def __or__(self, other: T) -> T:
        return SentinelValue(key=self.key, default=other)  # type: ignore[return-value]


@dataclass(kw_only=True, slots=True)
class SentinelValue:
    key: str | None
    default: Any


class SentinelFactory:

    def __getitem__(self, prop_key: str) -> Sentinel:
        return Sentinel(key=prop_key)


DEFAULT_PROPS = SentinelFactory()
DEFAULT_PROP = Sentinel(key=None)


def resolve_defaults(original_func: Callable[P, R]) -> Callable[P, R]:
    """This decorator makes the function resolve default properties set via ``default_props``.

    If a parameter has a default value which looks like ``DEFAULT_PROPS['prop-key'] | default_value``,
    the actual value will be taken from the element's ``_default_props`` dictionary with key "prop-key" if present,
    otherwise the specified ``default_value`` is used.

    If a parameter has a default value which looks like ``DEFAULT_PROP | default_value``,
    the dictionary key will be inferred from the parameter name (converting snake_case to kebab-case).
    """
    positional_kinds = {inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    sentinel_parameters = [
        (index if parameter.kind in positional_kinds else None, name, parameter.default)
        for index, (name, parameter) in enumerate(inspect.signature(original_func).parameters.items())
        if isinstance(parameter.default, SentinelValue)
    ]

    @functools.wraps(original_func)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> R:
        element = cast(Element, args[0])
        for index, name, default in sentinel_parameters:
            if index is not None and index < len(args):
                continue  # passed positionally
            value = kwargs.get(name, default)
            if isinstance(value, SentinelValue):
                key = value.key or name.replace('_', '-')
                kwargs[name] = element._default_props.get(key, value.default)  # pylint: disable=protected-access
        return original_func(*args, **kwargs)

    return decorated
