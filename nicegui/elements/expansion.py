from typing import Optional

from ..element import Element


class Expansion(Element):

    def __init__(self, text: str, *, icon: Optional[str] = None) -> None:
        '''Expansion Element

        Provides an expandable container.

        :param text: title text
        :param icon: optional icon (default: None)
        '''
        super().__init__('q-expansion-item')
        self._props['label'] = text
        self._props['icon'] = icon
