from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeGuard

from .helpers import is_coroutine_function

if TYPE_CHECKING:
    from .element import Element


class JsAction:
    """A callable action that can be optimized to run client-side via JavaScript.

    When passed to event handlers like ``on_click``, the action is executed
    on the client side via JavaScript, bypassing server-side latency. The event is
    also sent to the server so the Python callback runs and server state stays in sync.
    When called directly (e.g., ``dialog.open()``), it executes the Python implementation as usual.
    """

    def __init__(self, element: Element, python_fn: Callable[..., Any], js_handler: str) -> None:
        if is_coroutine_function(python_fn):
            raise TypeError(f'@js_action does not support async methods (got {python_fn!r})')
        self._element = element
        self._python_fn = python_fn
        self._js_handler = js_handler

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._python_fn(*args, **kwargs)

    def __repr__(self) -> str:
        return f'JsAction({self._element.__class__.__name__}.{self._python_fn.__name__})'

    def _call_without_loopback(self) -> Any:
        """Call the Python function without sending a redundant update to the client.

        Used when the action was already applied on the client via JavaScript.
        """
        element = self._element
        if hasattr(element, '_send_update_on_value_change'):
            prev = element._send_update_on_value_change  # pylint: disable=protected-access
            element._send_update_on_value_change = False  # pylint: disable=protected-access
            try:
                return self._python_fn()
            finally:
                element._send_update_on_value_change = prev  # pylint: disable=protected-access
        return self._python_fn()


class _JsActionDescriptor:
    """Descriptor that returns a JsAction when accessed on an element instance."""

    def __init__(self, method: Callable, js_handler_factory: Callable[[Any], str]) -> None:
        if is_coroutine_function(method):
            raise TypeError(f'@js_action does not support async methods (got {method!r})')
        self._method = method
        self._js_handler_factory = js_handler_factory
        for attr in functools.WRAPPER_ASSIGNMENTS:
            try:
                value = getattr(method, attr)
            except AttributeError:
                pass
            else:
                setattr(self, attr, value)
        self.__wrapped__ = method

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self._method
        bound = self._method.__get__(obj, objtype)
        return JsAction(obj, bound, self._js_handler_factory(obj))


class _JsActionFactory:
    """Decorator that marks a method as having a JS action equivalent.

    When the decorated method is passed as an event handler (e.g., ``on_click=dialog.open``),
    the JS handler runs on the client side for instant response, while the Python method
    also runs on the server to keep state in sync.

    Use the convenience constructors ``js_action.value()`` and ``js_action.toggle()``
    for common model-value operations.
    """

    def __call__(self, js_handler_factory: Callable[[Any], str]) -> Callable[[Callable[..., Any]], _JsActionDescriptor]:
        def decorator(method: Callable[..., Any]) -> _JsActionDescriptor:
            return _JsActionDescriptor(method, js_handler_factory)
        return decorator

    def value(self, v: bool) -> Callable[[Callable[..., Any]], _JsActionDescriptor]:
        """Create a decorator that sets the model-value prop to the given value."""
        js_bool = 'true' if v else 'false'
        return self(lambda el: (
            f'(...args) => {{ elements[{el.id}].props["model-value"] = {js_bool}; emit(...args); }}'
        ))

    def toggle(self) -> Callable[[Callable[..., Any]], _JsActionDescriptor]:
        """Create a decorator that toggles the model-value prop."""
        return self(lambda el: (
            f'(...args) => {{ const e = elements[{el.id}]; '
            f'e.props["model-value"] = !e.props["model-value"]; emit(...args); }}'
        ))


js_action = _JsActionFactory()


def has_js_action(handler: Any) -> TypeGuard[JsAction]:
    """Check if a handler is a JsAction."""
    return isinstance(handler, JsAction)
