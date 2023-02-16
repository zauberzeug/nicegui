from typing import Any, Callable, Optional

from .. import globals
from ..element import Element
from .mixins.value_element import ValueElement


class Tabs(ValueElement):

    def __init__(self, *,
                 value: Any = None,
                 on_change: Optional[Callable] = None) -> None:
        """Tabs

        This element represents `Quasar's QTabs <https://quasar.dev/vue-components/tabs#qtabs-api>`_ component.
        It contains individual tabs.

        :param value: name of the tab to be initially selected
        :param on_change: callback to be executed when the selected tab changes
        """
        super().__init__(tag='q-tabs', value=value, on_value_change=on_change)
        self.panels: Optional[TabPanels] = None


class Tab(Element):

    def __init__(self, name: str, label: Optional[str] = None, icon: Optional[str] = None) -> None:
        """Tab

        This element represents `Quasar's QTab <https://quasar.dev/vue-components/tabs#qtab-api>`_ component.
        It is a child of a `Tabs` element.

        :param name: name of the tab (the value of the `Tabs` element)
        :param label: label of the tab (default: `None`, meaning the same as `name`)
        :param icon: icon of the tab (default: `None`)
        """
        super().__init__('q-tab')
        self._props['name'] = name
        self._props['label'] = label if label is not None else name
        if icon:
            self._props['icon'] = icon
        self.tabs = globals.get_slot().parent


class TabPanels(ValueElement):

    def __init__(self,
                 tabs: Tabs, *,
                 value: Any = None,
                 on_change: Optional[Callable] = None,
                 animated: bool = True,
                 ) -> None:
        """Tab Panels

        This element represents `Quasar's QTabPanels <https://quasar.dev/vue-components/tab-panels#qtabpanels-api>`_ component.
        It contains individual tab panels.

        :param tabs: the `Tabs` element that controls this element
        :param value: name of the tab panel to be initially visible
        :param on_change: callback to be executed when the visible tab panel changes
        :param animated: whether the tab panels should be animated (default: `True`)
        """
        super().__init__(tag='q-tab-panels', value=value, on_value_change=on_change)
        tabs.bind_value(self, 'value')
        self._props['animated'] = animated


class TabPanel(Element):

    def __init__(self, name: str) -> None:
        """Tab Panel

        This element represents `Quasar's QTabPanel <https://quasar.dev/vue-components/tab-panels#qtabpanel-api>`_ component.
        It is a child of a `TabPanels` element.

        :param name: name of the tab panel (the value of the `TabPanels` element)
        """
        super().__init__('q-tab-panel')
        self._props['name'] = name
