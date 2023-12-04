from dataclasses import dataclass, field
from typing import Callable, List, Optional

from nicegui.dataclasses import KWONLY_SLOTS

from .part import DocumentationPart


@dataclass(**KWONLY_SLOTS)
class DocumentationPage:
    name: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    back_link: Optional[str] = None
    parts: List[DocumentationPart] = field(default_factory=list)
    extra_column: Optional[Callable] = None

    @property
    def heading(self) -> str:
        """Return the heading of the page."""
        return self.title or self.parts[0].title or ''
