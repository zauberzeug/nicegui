from .. import helpers
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .tabs import Tabs


class Tab(LabelElement, IconElement, DisableableElement):

    def __init__(self, name: str, label: str | None = None, icon: str | None = None) -> None:
        """Tab

        This element represents `Quasar's QTab <https://quasar.dev/vue-components/tabs#qtab-api>`_ component.
        It is a direct or indirect child of a `ui.tabs` element.

        :param name: name of the tab (will be the value of the `ui.tabs` element)
        :param label: label of the tab (default: `None`, meaning the same as `name`)
        :param icon: icon of the tab (default: `None`)
        """
        if label is None:
            label = name
        super().__init__(tag='q-tab', label=label, icon=icon)
        self._props['name'] = name
        self.tabs = next(
            (e for e in self.ancestors() if isinstance(e, Tabs)),
            None,  # DEPRECATED: raise an error in NiceGUI 4.0 if no ui.tabs ancestor is found
        )
        if self.tabs is None:
            helpers.warn_once('A ui.tab should be a child of a ui.tabs element. '
                              'This will raise an error in NiceGUI 4.0.')
