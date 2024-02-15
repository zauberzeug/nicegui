
from dataclasses import dataclass
from typing import Callable, Literal, Optional, Union

from nicegui.dataclasses import KWONLY_SLOTS

from ....style import create_anchor_name


@dataclass(**KWONLY_SLOTS)
class Demo:
    """
    A demo class representing a function with optional lazy evaluation and tab information.

    Attributes:
        function (Callable): The function to be executed.
        lazy (bool, optional): Whether the function should be lazily evaluated. Defaults to True.
        tab (Optional[Union[str, Callable]], optional): The tab information for the demo. Defaults to None.
    """

    function: Callable
    lazy: bool = True
    tab: Optional[Union[str, Callable]] = None


@dataclass(**KWONLY_SLOTS)
class DocumentationPart:
    """
    Represents a part of the documentation.

    Attributes:
        title (Optional[str]): The title of the documentation part.
        description (Optional[str]): The description of the documentation part.
        description_format (Literal['md', 'rst']): The format of the description (markdown or reStructuredText).
        link (Optional[str]): The link associated with the documentation part.
        ui (Optional[Callable]): The user interface function associated with the documentation part.
        demo (Optional[Demo]): The demo associated with the documentation part.
        reference (Optional[type]): The reference type associated with the documentation part.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    description_format: Literal['md', 'rst'] = "md"
    link: Optional[str] = None
    ui: Optional[Callable] = None
    demo: Optional[Demo] = None
    reference: Optional[type] = None

    @property
    def link_target(self) -> Optional[str]:
        """
        Return the link target for in-page navigation.

        Returns:
            Optional[str]: The link target for in-page navigation, or None if no title is provided.
        """
        return create_anchor_name(self.title) if self.title else None
