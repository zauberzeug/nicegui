from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from nicegui.dataclasses import KWONLY_SLOTS

from ....style import create_anchor_name


@dataclass(**KWONLY_SLOTS)
class Demo:
    function: Callable
    lazy: bool = True
    tab: str | Callable | None = None


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    title: str | None = None
    description: str | None = None
    description_format: Literal['md', 'rst'] = 'md'
    link: str | None = None
    ui: Callable | None = None
    demo: Demo | None = None
    reference: type | None = None
    search_text: str | None = None
    children: list['DocumentationPart'] = field(default_factory=list)

    @property
    def link_target(self) -> str | None:
        """Return the link target for in-page navigation."""
        return create_anchor_name(self.title) if self.title else None
