from typing_extensions import Self

from .value_element import ValueElement


class OpenableElement(ValueElement[bool]):

    def open(self) -> Self:
        """Open the element."""
        self.value = True
        return self

    def close(self) -> Self:
        """Close the element."""
        self.value = False
        return self

    def toggle(self) -> Self:
        """Toggle the element."""
        self.value = not self.value
        return self

    def _render_markdown(self) -> str:
        return self._children_to_markdown() if self.value else ''
