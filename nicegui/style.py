import weakref
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generic, TypeVar

from .observables import ObservableDict

if TYPE_CHECKING:
    from .element import Element

T = TypeVar('T', bound='Element')


class Style(ObservableDict, Generic[T]):

    def __init__(self, *args, element: T, **kwargs) -> None:
        super().__init__(*args, on_change=self._update, **kwargs)
        self._element = weakref.ref(element)
        self._suspend_count = 0

    @contextmanager
    def suspend_updates(self) -> Iterator[None]:
        """Suspend updates."""
        self._suspend_count += 1
        try:
            yield
        finally:
            self._suspend_count -= 1

    @property
    def element(self) -> T:
        """The element this style object belongs to."""
        element = self._element()
        if element is None:
            raise RuntimeError('The element this style object belongs to has been deleted.')
        return element

    def _update(self) -> None:
        if self._suspend_count > 0:
            return
        element = self._element()
        if element is not None:
            element.update()

    def __call__(self,
                 add: str | None = None, *,
                 remove: str | None = None,
                 replace: str | None = None) -> T:
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
        return element

    @staticmethod
    def parse(text: str | None) -> dict[str, str]:
        """Parse a string of styles into a dictionary."""
        result = {}
        for word in (text or '').split(';'):
            word = word.strip()  # noqa: PLW2901
            if word:
                key, value = word.split(':', 1)
                result[key.strip()] = value.strip()
        return result
