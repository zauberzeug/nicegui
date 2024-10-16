from __future__ import annotations

from typing import Any, Optional, Union

from ..context import context
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.value_element import ValueElement


class Tabs(ValueElement):

    def __init__(self, *,
                 value: Union[Tab, TabPanel, None] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """Tabs

        This element represents `Quasar's QTabs <https://quasar.dev/vue-components/tabs#qtabs-api>`_ component.
        It contains individual tabs.

        :param value: `ui.tab`, `ui.tab_panel`, or name of the tab to be initially selected
        :param on_change: callback to be executed when the selected tab changes
        """
        super().__init__(tag='q-tabs', value=value, on_value_change=on_change)

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value


class Tab(IconElement, DisableableElement):

    def __init__(self, name: str, label: Optional[str] = None, icon: Optional[str] = None) -> None:
        """Tab

        This element represents `Quasar's QTab <https://quasar.dev/vue-components/tabs#qtab-api>`_ component.
        It is a child of a `ui.tabs` element.

        :param name: name of the tab (will be the value of the `ui.tabs` element)
        :param label: label of the tab (default: `None`, meaning the same as `name`)
        :param icon: icon of the tab (default: `None`)
        """
        super().__init__(tag='q-tab', icon=icon)
        self._props['name'] = name
        self._props['label'] = label if label is not None else name
        self.tabs = context.slot.parent


class TabPanels(ValueElement):

    def __init__(self,
                 tabs: Optional[Tabs] = None, *,
                 value: Union[Tab, TabPanel, str, None] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 animated: bool = True,
                 keep_alive: bool = True,
                 ) -> None:
        """Tab Panels

        This element represents `Quasar's QTabPanels <https://quasar.dev/vue-components/tab-panels#qtabpanels-api>`_ component.
        It contains individual tab panels.

        To avoid issues with dynamic elements when switching tabs,
        this element uses Vue's `keep-alive <https://vuejs.org/guide/built-ins/keep-alive.html>`_ component.
        If client-side performance is an issue, you can disable this feature.

        :param tabs: an optional `ui.tabs` element that controls this element
        :param value: `ui.tab`, `ui.tab_panel`, or name of the tab panel to be initially visible
        :param on_change: callback to be executed when the visible tab panel changes
        :param animated: whether the tab panels should be animated (default: `True`)
        :param keep_alive: whether to use Vue's keep-alive component on the content (default: `True`)
        """
        super().__init__(tag='q-tab-panels', value=value, on_value_change=on_change)
        if tabs is not None:
            tabs.bind_value(self, 'value')
        self._props['animated'] = animated
        self._props['keep-alive'] = keep_alive

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value


class TabPanel(DisableableElement, default_classes='nicegui-tab-panel'):

    def __init__(self, name: Union[Tab, str]) -> None:
        """Tab Panel

        This element represents `Quasar's QTabPanel <https://quasar.dev/vue-components/tab-panels#qtabpanel-api>`_ component.
        It is a child of a `TabPanels` element.

        :param name: `ui.tab` or the name of a tab element
        """
        super().__init__(tag='q-tab-panel')
        self._props['name'] = name.props['name'] if isinstance(name, Tab) else name
