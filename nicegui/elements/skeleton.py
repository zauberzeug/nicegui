
from ..element import Element


class Skeleton(Element):
    def __init__(self, type : str):
        """Skeleton

        This element is based on Quasar's `QSkeleton <https://quasar.dev/vue-components/skeleton>`_ component.

        It serves as a placeholder for loading content in cards, menus and other component containers.

        :param type: the type of skeleton to display. Valid options can be found here: https://quasar.dev/vue-components/skeleton/#predefined-types
        """

        super().__init__('q-skeleton')
        self._props['type'] = type
