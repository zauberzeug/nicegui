
from dataclasses import dataclass
from typing import Callable, Literal, Optional, Union

from nicegui.dataclasses import KWONLY_SLOTS

from ....style import create_anchor_name


@dataclass(**KWONLY_SLOTS)
class Demo:
    function: Callable
    lazy: bool = True
    tab: Optional[Union[str, Callable]] = None


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    title: Optional[str] = None
    description: Optional[str] = None
    description_format: Literal['md', 'rst'] = 'md'
    link: Optional[str] = None
    ui: Optional[Callable] = None
    demo: Optional[Demo] = None
    reference: Optional[type] = None

    @property
    def link_target(self) -> Optional[str]:
        """Return the link target for in-page navigation."""
        return create_anchor_name(self.title) if self.title else None
