import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from inspect import Parameter
from typing import Any, NamedTuple, TypeVar

from typing_extensions import ParamSpec

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


class _DefaultPropParam(NamedTuple):
    name: str
    prop_key: str
    fallback_value: Any
    positional_arg_index: int | None
    positional_only: bool


def _resolve_sentinel_value(default_props: dict[str, Any], parameter_name: str, value: SentinelValue) -> Any:
    key = value.key or parameter_name.replace('_', '-')
    return default_props.get(key, value.default)


def _default_prop_params(signature: inspect.Signature) -> tuple[_DefaultPropParam, ...]:
    default_prop_params: list[_DefaultPropParam] = []
    positional_index = 0

    for parameter in signature.parameters.values():
        if parameter.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
            parameter_positional_index = positional_index
            positional_index += 1
        else:
            parameter_positional_index = None

        default = parameter.default
        if not isinstance(default, SentinelValue):
            continue

        default_prop_params.append(_DefaultPropParam(
            name=parameter.name,
            prop_key=default.key or parameter.name.replace('_', '-'),
            fallback_value=default.default,
            positional_arg_index=parameter_positional_index,
            positional_only=parameter.kind is Parameter.POSITIONAL_ONLY,
        ))

    return tuple(default_prop_params)


def _fallback_kwargs_by_arg_count(
    signature: inspect.Signature,
    default_prop_params: tuple[_DefaultPropParam, ...],
) -> tuple[dict[str, Any], ...]:
    """Precompute fallback kwargs for calls without custom default props.

    The tuple index is the number of positional arguments supplied to the decorated function.
    """
    positional_parameter_count = sum(
        1
        for parameter in signature.parameters.values()
        if parameter.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
    )
    return tuple(
        {
            param.name: param.fallback_value
            for param in default_prop_params
            if param.positional_arg_index is None or param.positional_arg_index >= arg_count
        }
        for arg_count in range(positional_parameter_count + 1)
    )


def _resolve_defaults_via_signature_bind(original_func: Callable[P, R], signature: inspect.Signature,
                                         default_prop_params: tuple[_DefaultPropParam, ...],
                                         args: tuple[Any, ...], kwargs: dict[str, Any]) -> R:
    bound_arguments = signature.bind(*args, **kwargs)
    bound_arguments.apply_defaults()

    element: Element = bound_arguments.arguments['self']
    default_props = element._default_props  # pylint: disable=protected-access

    for param in default_prop_params:
        value = bound_arguments.arguments[param.name]
        if isinstance(value, SentinelValue):
            bound_arguments.arguments[param.name] = _resolve_sentinel_value(default_props, param.name, value)
    return original_func(*bound_arguments.args, **bound_arguments.kwargs)


def resolve_defaults(original_func: Callable[P, R]) -> Callable[P, R]:
    """This decorator makes the function resolve default properties set via ``default_props``.

    If a parameter has a default value which looks like ``DEFAULT_PROPS['prop-key'] | default_value``,
    the actual value will be taken from the element's ``_default_props`` dictionary with key "prop-key" if present,
    otherwise the specified ``default_value`` is used.

    If a parameter has a default value which looks like ``DEFAULT_PROP | default_value``,
    the dictionary key will be inferred from the parameter name (converting snake_case to kebab-case).
    """
    signature = inspect.signature(original_func)
    default_prop_params = _default_prop_params(signature)
    has_positional_only_default_props = any(param.positional_only for param in default_prop_params)
    fallback_kwargs_by_arg_count = _fallback_kwargs_by_arg_count(signature, default_prop_params)
    positional_default_prop_indices: tuple[int, ...] = tuple(
        param.positional_arg_index
        for param in default_prop_params
        if param.positional_arg_index is not None
    )

    @functools.wraps(original_func)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> R:
        """Resolve default property sentinels efficiently.

        Common constructor calls can resolve omitted sentinels without normalizing every argument.
        Two cases require the slower ``Signature.bind`` path:

        1. Positional-only default-prop params can't be injected via kwargs.
        2. No positional args and no explicit ``self`` kwarg — we can't locate the element to read ``_default_props``.

        :param args: positional arguments forwarded to the original function
        :param kwargs: keyword arguments forwarded to the original function
        :return: return value of the original function with resolved defaults
        """
        needs_full_signature_bind = has_positional_only_default_props or (not args and 'self' not in kwargs)
        if needs_full_signature_bind:
            return _resolve_defaults_via_signature_bind(original_func, signature, default_prop_params, args, kwargs)

        element: Element = args[0] if args else kwargs['self']  # type: ignore[assignment]
        default_props = element._default_props  # pylint: disable=protected-access
        arg_count = len(args)
        # Fast path: when no custom default_props or kwargs exist and no positional arg
        # is itself a SentinelValue, use the precomputed fallback table (no Signature.bind).
        can_skip_resolution = not default_props and not kwargs
        if can_skip_resolution and arg_count < len(fallback_kwargs_by_arg_count):
            for supplied_arg_index in positional_default_prop_indices:
                if supplied_arg_index < arg_count and isinstance(args[supplied_arg_index], SentinelValue):
                    return _resolve_defaults_via_signature_bind(original_func, signature, default_prop_params,
                                                                args, kwargs)
            return original_func(*args, **fallback_kwargs_by_arg_count[arg_count])

        for parameter_name, prop_key, fallback_value, positional_arg_index, _positional_only in default_prop_params:
            if parameter_name in kwargs:
                value = kwargs[parameter_name]
                if isinstance(value, SentinelValue):
                    kwargs[parameter_name] = (_resolve_sentinel_value(default_props, parameter_name, value)
                                              if default_props else value.default)
                continue
            if positional_arg_index is not None and positional_arg_index < arg_count:
                if isinstance(args[positional_arg_index], SentinelValue):
                    # Explicit positional sentinels need Signature.bind() so the rebuilt call uses resolved values.
                    return _resolve_defaults_via_signature_bind(original_func, signature, default_prop_params,
                                                                args, kwargs)
                continue
            kwargs[parameter_name] = default_props.get(prop_key, fallback_value) if default_props else fallback_value
        return original_func(*args, **kwargs)

    return decorated
