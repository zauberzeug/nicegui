from __future__ import annotations

from typing import Any

from ..context import context
from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class Tabs(ValueElement):

    def __init__(self, *,
                 value: Tab | TabPanel | None = None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 ) -> None:
        """Tabs

        This element represents `Quasar's QTabs <https://quasar.dev/vue-components/tabs#qtabs-api>`_ component.
        It contains individual tabs.

        :param value: `ui.tab`, `ui.tab_panel`, or name of the tab to be initially selected
        :param on_change: callback to be executed when the selected tab changes (*since version 3.6.0*: event ``value`` is the tab name)
        """
        super().__init__(tag='q-tabs', value=value, on_value_change=on_change)

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value

    def _value_to_event_value(self, value: Any) -> Any:
        return self._value_to_model_value(value)


class Tab(LabelElement, IconElement, DisableableElement):

    def __init__(self, name: str, label: str | None = None, icon: str | None = None) -> None:
        """Tab

        This element represents `Quasar's QTab <https://quasar.dev/vue-components/tabs#qtab-api>`_ component.
        It is a child of a `ui.tabs` element.

        :param name: name of the tab (will be the value of the `ui.tabs` element)
        :param label: label of the tab (default: `None`, meaning the same as `name`)
        :param icon: icon of the tab (default: `None`)
        """
        if label is None:
            label = name
        super().__init__(tag='q-tab', label=label, icon=icon)
        self._props['name'] = name
        self.tabs = context.slot.parent


class TabPanels(ValueElement):

    @resolve_defaults
    def __init__(self,
                 tabs: Tabs | None = None, *,
                 value: Tab | TabPanel | str | None = None,
                 on_change: Handler[ValueChangeEventArguments] | None = None,
                 animated: bool = DEFAULT_PROP | True,
                 keep_alive: bool = DEFAULT_PROP | True,
                 ) -> None:
        """Tab Panels

        This element represents `Quasar's QTabPanels <https://quasar.dev/vue-components/tab-panels#qtabpanels-api>`_ component.
        It contains individual tab panels.

        To avoid issues with dynamic elements when switching tabs,
        this element uses Vue's `keep-alive <https://vuejs.org/guide/built-ins/keep-alive.html>`_ component.
        If client-side performance is an issue, you can disable this feature.

        :param tabs: an optional `ui.tabs` element that controls this element
        :param value: `ui.tab`, `ui.tab_panel`, or name of the tab panel to be initially visible
        :param on_change: callback to be executed when the visible tab panel changes (*since version 3.6.0*: event ``value`` is the tab name)
        :param animated: whether the tab panels should be animated (default: `True`)
        :param keep_alive: whether to use Vue's keep-alive component on the content (default: `True`)
        """
        super().__init__(tag='q-tab-panels', value=value, on_value_change=on_change)
        if tabs is not None:
            tabs.bind_value(self, 'value')
        self._props.set_bool('animated', animated)
        self._props.set_bool('keep-alive', keep_alive)

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value

    def _value_to_event_value(self, value: Any) -> Any:
        return self._value_to_model_value(value)


class TabPanel(DisableableElement, default_classes='nicegui-tab-panel'):

    def __init__(self, name: Tab | str) -> None:
        """Tab Panel

        This element represents `Quasar's QTabPanel <https://quasar.dev/vue-components/tab-panels#qtabpanel-api>`_ component.
        It is a child of a `TabPanels` element.

        :param name: `ui.tab` or the name of a tab element
        """
        super().__init__(tag='q-tab-panel')
        self._props['name'] = name.props['name'] if isinstance(name, Tab) else name
