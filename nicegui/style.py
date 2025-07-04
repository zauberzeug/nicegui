import weakref
from typing import TYPE_CHECKING, Dict, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from .element import Element

T = TypeVar('T', bound='Element')


class Style(dict, Generic[T]):

    def __init__(self, *args, element: T, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._element = weakref.ref(element)

    @property
    def element(self) -> T:
        """The element this style object belongs to."""
        element = self._element()
        if element is None:
            raise RuntimeError('The element this style object belongs to has been deleted.')
        return element

    def __call__(self,
                 add: Optional[str] = None, *,
                 remove: Optional[str] = None,
                 replace: Optional[str] = None) -> T:
        """Apply, remove, or replace CSS definitions.

        Removing or replacing styles can be helpful if the predefined style is not desired.

        :param add: semicolon-separated list of styles to add to the element
        :param remove: semicolon-separated list of styles to remove from the element
        :param replace: semicolon-separated list of styles to use instead of existing ones
        """
        element = self.element
        style_dict = {**self} if replace is None else {}
        for key in self.parse(remove):
            style_dict.pop(key, None)
        style_dict.update(self.parse(add))
        style_dict.update(self.parse(replace))
        if self != style_dict:
            self.clear()
            self.update(style_dict)
            element.update()
        return element

    @staticmethod
    def parse(text: Optional[str]) -> Dict[str, str]:
        """Parse a string of styles into a dictionary."""
        result = {}
        for word in (text or '').split(';'):
            word = word.strip()  # noqa: PLW2901
            if word:
                key, value = word.split(':', 1)
                result[key.strip()] = value.strip()
        return result
