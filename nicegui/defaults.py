import functools
import inspect
from collections.abc import Callable
from typing import Any, TypeVar

from typing_extensions import ParamSpec

from .element import Element

T = TypeVar('T')

P = ParamSpec('P')
R = TypeVar('R')


class DEFAULT_PROPS:

    def __init__(self, prop_key: str) -> None:
        self.key = prop_key
        self.default: Any

    def __or__(self, other: T) -> T:
        self.default = other  # type: ignore[assignment]
        return self  # type: ignore[return-value]


def honor_default_props(original_func: Callable[P, R]) -> Callable[P, R]:
    """This decorator makes the function honor default properties set via ``default_props``.

    If a parameter has a default value which looks like ``DEFAULT_PROPS('prop_key') | default_value``,
    the actual value will be taken from the element's ``_default_props`` dictionary with key ``prop_key`` if present,
    otherwise the specified ``default_value`` is used.
    """
    signature = inspect.signature(original_func)

    @functools.wraps(original_func)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> R:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        element: Element = bound.arguments['self']

        return original_func(*bound.args, **{
            param_name: (element._default_props.get(value.key, value.default)  # pylint: disable=protected-access
                         if isinstance(value, DEFAULT_PROPS) else value)
            for param_name, value in bound.arguments.items()
        })

    return decorated
