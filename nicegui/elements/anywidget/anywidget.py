from __future__ import annotations

import importlib.util
import inspect
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Tuple

from ... import optional_features
from ..mixins.value_element import ValueElement

if importlib.util.find_spec('anywidget'):
    optional_features.register('anywidget')
    if TYPE_CHECKING:
        import anywidget


class AnyWidget(ValueElement,
                component='anywidget.js',
                dependencies=['widget.js'],
                default_classes='nicegui-anywidget'):

    VALUE_PROP: str = 'traits'

    def __init__(self,
                 widget: anywidget.AnyWidget,
                 **kwargs: Any,
                 ) -> None:
        """Anywidget

        `anywidget <https://anywidget.dev/en/getting-started/>`_ is a library that allows you to
        embed arbitrary JavaScript widgets in a cross-frontend friendly manner.

        There are many publicly available examples of `anywidget` widgets
        in the `anywidget gallery <https://try.anywidget.dev/>`_, including
        `altair.JupyterChart <https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html>`_,
        and `quak <https://github.com/manzt/quak>`_.

        Implementation: The `nicegui.anywidget` element takes an `Anywidget` and observes all `sync=True` traits
        of the widget, trigger JS updates when the traits change.
        Conversely, changes on the frontend will be synced back to the widget,
        using `ValueElement`'s handling to listen to changes on `traits`.

        :param widget: the `anywidget.AnyWidget` to wrap
        :param throttle: minimum time (in seconds) between widget updates to python (default: 0.0)
        """
        self._widget = widget
        traits = self.get_traits(widget)
        super().__init__(value=traits, **kwargs)
        self._props['esm_content'], self._props['css_content'] = self.get_esm_css(widget)
        self._props['_debug'] = False  # set to True for console logging

        # Observe all widget traits and fire update_trait() JS method when changed in python
        for trait in traits:
            def update_trait(change, trait=trait):
                self.run_method('update_trait', {'trait': trait, 'new': change['new'], 'old': change['old']})
            self._widget.observe(update_trait, trait)
        self._update_method = 'update_traits'

    @classmethod
    def get_esm_css(cls, widget_instance: anywidget.AnyWidget) -> Tuple[str, str]:
        """Extract the widget's ESM and CSS content, reading if they are `Path` objects"""
        # Get the ESM module content
        esm_content = getattr(widget_instance, '_esm')

        # Check if ESM content is a property function (sometimes the case in anywidget)
        if callable(esm_content) and not inspect.isclass(esm_content):
            esm_content = esm_content()

        # Get CSS content if available
        css_content = None
        if hasattr(widget_instance, '_css'):
            css_attr = getattr(widget_instance, '_css')
            if callable(css_attr) and not inspect.isclass(css_attr):
                css_content = css_attr()
            else:
                css_content = css_attr

        if isinstance(esm_content, str) and os.path.exists(esm_content):
            esm_content = Path(esm_content)
        if isinstance(css_content, str) and os.path.exists(css_content):
            css_content = Path(css_content)

        if isinstance(esm_content, os.PathLike):
            with open(esm_content, 'r') as f:
                esm_content = f.read()
        if isinstance(css_content, os.PathLike):
            with open(css_content, 'r') as f:
                css_content = f.read()
        return esm_content or '', css_content or ''

    @classmethod
    def get_traits(cls, widget_instance: anywidget.AnyWidget) -> dict[str, Any]:
        """Extract the widget's current state - only get traits marked with `sync=True`"""
        sync_traits = list(widget_instance.traits(sync=True))
        # get_state() will access the trait values and serialize to JSON if needed
        # https://ipywidgets.readthedocs.io/en/latest/_modules/ipywidgets/widgets/widget.html#Widget.get_state
        return widget_instance.get_state(key=sync_traits)

    def _handle_value_change(self, value: Any) -> None:
        """Update the widget's state when the value changes from frontend"""
        super()._handle_value_change(value)
        # TODO: currently this is iterating all traits and doing extra JSON serialization.
        # Ideally we would directly have the frontend tell us which traits have changed?
        current_traits = self.get_traits(self._widget)
        for key, value_ in value.items():
            if current_traits[key] != value_:
                setattr(self._widget, key, value_)
        if self._send_update_on_value_change:
            self.run_method('update_traits')
