from typing import Any

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement
from .tab import Tab
from .tab_panel import TabPanel
from .tabs import Tabs


class TabPanels(ValueElement[str | Tab | TabPanel | None]):

    @resolve_defaults
    def __init__(self,
                 tabs: Tabs | None = None, *,
                 value: Tab | TabPanel | str | None = None,
                 on_change: Handler[ValueChangeEventArguments[str | Tab | TabPanel | None]] | None = None,
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

    def _value_to_model_value(self, value: Any) -> str | None:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value

    def _value_to_event_value(self, value: Any) -> str | None:
        return self._value_to_model_value(value)
