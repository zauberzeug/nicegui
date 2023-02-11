from typing import Optional

from .mixins.value_element import ValueElement


class Expansion(ValueElement):

    def __init__(self, text: str, *, icon: Optional[str] = None, value: bool = False) -> None:
        '''Expansion Element

        Provides an expandable container.

        :param text: title text
        :param icon: optional icon (default: None)
        :param value: whether the expansion should be opened on creation (default: `False`)
        '''
        super().__init__(tag='q-expansion-item', value=value, on_value_change=None)
        self._props['label'] = text
        self._props['icon'] = icon

    def open(self) -> None:
        self.value = True

    def close(self) -> None:
        self.value = False
