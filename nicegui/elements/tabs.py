from typing import Any

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement
from .tab import Tab
from .tab_panel import TabPanel


class Tabs(ValueElement[str | Tab | TabPanel | None]):

    def __init__(self, *,
                 value: Tab | TabPanel | None = None,
                 on_change: Handler[ValueChangeEventArguments[str | Tab | TabPanel | None]] | None = None,
                 ) -> None:
        """Tabs

        This element represents `Quasar's QTabs <https://quasar.dev/vue-components/tabs#qtabs-api>`_ component.
        It contains individual tabs.

        :param value: `ui.tab`, `ui.tab_panel`, or name of the tab to be initially selected
        :param on_change: callback to be executed when the selected tab changes (*since version 3.6.0*: event ``value`` is the tab name)
        """
        super().__init__(tag='q-tabs', value=value, on_value_change=on_change)

    def _value_to_model_value(self, value: Any) -> str | None:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value

    def _value_to_event_value(self, value: Any) -> str | None:
        return self._value_to_model_value(value)
