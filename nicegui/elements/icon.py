from typing import Optional

from ..element import Element


class Icon(Element):

    def __init__(self,
                 name: str,
                 *,
                 size: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        """Icon

        This element is based on Quasar's `QIcon <https://quasar.dev/vue-components/icon>`_ component.

        `Here <https://material.io/icons/>`_ is a reference of possible names.

        :param name: name of the icon
        :param size: size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl), examples: 16px, 2rem
        :param color: color name for component, examples: primary, teal-10
        """
        super().__init__('q-icon')
        self._props['name'] = name

        if size:
            self._props['size'] = size

        if color:
            self._props['color'] = color
