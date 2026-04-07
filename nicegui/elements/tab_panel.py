from .mixins.disableable_element import DisableableElement
from .tab import Tab


class TabPanel(DisableableElement, default_classes='nicegui-tab-panel'):

    def __init__(self, name: Tab | str) -> None:
        """Tab Panel

        This element represents `Quasar's QTabPanel <https://quasar.dev/vue-components/tab-panels#qtabpanel-api>`_ component.
        It is a child of a `TabPanels` element.

        :param name: `ui.tab` or the name of a tab element
        """
        super().__init__(tag='q-tab-panel')
        self._props['name'] = name.props['name'] if isinstance(name, Tab) else name
