from dataclasses import dataclass, field
from collections.abc import Callable

from nicegui.dataclasses import KWONLY_SLOTS

from .part import DocumentationPart


@dataclass(**KWONLY_SLOTS)
class DocumentationPage:
    name: str
    title: str | None = None
    subtitle: str | None = None
    back_link: str | None = None
    parts: list[DocumentationPart] = field(default_factory=list)
    extra_column: Callable | None = None

    @property
    def heading(self) -> str:
        """Return the heading of the page."""
        return self.title or self.parts[0].title or ''
