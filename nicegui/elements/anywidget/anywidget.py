from __future__ import annotations

import importlib.util
import inspect
import math
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ... import helpers, optional_features
from ..mixins.value_element import ValueElement

if importlib.util.find_spec('anywidget'):
    optional_features.register('anywidget')
    if TYPE_CHECKING:
        import anywidget

UNDEFINED = object()


class AnyWidget(ValueElement, component='anywidget.js', dependencies=['lib/widget.js']):
    VALUE_PROP: str = 'traits'

    def __init__(self, widget: anywidget.AnyWidget, *, throttle: float = 0) -> None:
        """AnyWidget

        `anywidget <https://anywidget.dev/en/getting-started/>`_ is a library that allows you to
        embed arbitrary JavaScript widgets in a cross-frontend friendly manner.

        There are many publicly available examples of anywidget widgets
        in the `anywidget gallery <https://try.anywidget.dev/>`_, including
        `altair.JupyterChart <https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html>`_,
        and `quak <https://github.com/manzt/quak>`_.

        Implementation: The ``nicegui.anywidget`` element takes an ``AnyWidget`` and observes all ``sync=True`` traits
        of the widget, trigger JS updates when the traits change.
        Conversely, changes on the frontend will be synced back to the widget,
        using ``ValueElement``'s handling to listen to changes on ``traits``.

        *Added in version 3.5.0*

        :param widget: the ``anywidget.AnyWidget`` to wrap
        :param throttle: minimum time (in seconds) between widget updates to Python (default: 0.0)
        """
        self._widget = widget
        self._traits = widget.traits(sync=True)
        super().__init__(value=widget.get_state(self._traits), throttle=throttle)
        self._props['esm_content'] = _get_attribute(widget, '_esm')
        self._props['css_content'] = _get_attribute(widget, '_css')
        self._state_lock: dict | None = None  # only used while handling a value change from the client

        def observe_change(change) -> None:
            """Observe a trait change and update the frontend (but avoid echoing same values back to the client)."""
            name = change['name']
            new = change['new']
            if self._state_lock is None:
                # we're not handling a value change from the client, so we send an update to the client
                self.run_method('update_trait', name, new)
            elif not _equal(self._state_lock.get(name, UNDEFINED), new):
                # an observer changed a trait to a new value, so we update the lock and send an update to the client
                self._state_lock[name] = new
                self.run_method('update_trait', name, new)

        widget.observe(observe_change, self._traits)

    def _handle_value_change(self, value: Any) -> None:
        """Update the widget's state when the value changes from frontend"""
        self._state_lock = value
        try:
            super()._handle_value_change(value)
            state = self._widget.get_state(self._traits)
            for key, value_ in value.items():
                if state[key] != value_:
                    setattr(self._widget, key, value_)
        finally:
            self._state_lock = None


def _get_attribute(obj: object, name: str) -> str:
    """Extract the attribute's content, reading if it is a path to a file."""
    content = getattr(obj, name, '')
    if callable(content) and not inspect.isclass(content):  # content is a property function
        content = content()
    assert isinstance(content, (str, Path)), f'Attribute {name} is not a string or Path'
    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf8')
    assert isinstance(content, str), f'Attribute {name} is a Path but does not exist'
    return content


def _equal(a: Any, b: Any) -> bool:
    """Check if two values are equal, considering NaN as equal."""
    if a == b:
        return True
    try:
        return math.isnan(a) and math.isnan(b)
    except TypeError:
        return False
