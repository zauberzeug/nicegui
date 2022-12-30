from typing import Callable, Union

from .. import globals
from ..element import Element
from .mixins.text_element import TextElement


class Link(TextElement):

    def __init__(self, text: str = '', target: Union[Callable, str] = '#') -> None:
        """Link

        Create a hyperlink.

        To jump to a specific location within a page you can place linkable anchors with `ui.link_target("name")`
        and link to it with `ui.link(target="#name")`.

        :param text: display text
        :param target: page function or string that is a an absolute URL or relative path from base URL
        """
        super().__init__(tag='a', text=text)
        self._props['href'] = target if isinstance(target, str) else globals.page_routes[target]
        self._classes.extend(['underline', 'text-blue'])


class LinkTarget(Element):

    def __init__(self, name: str) -> None:
        """Link target

        Create an anchor tag that can be used as inner-page target for links.

        :param name: target name
        """
        super().__init__('a')
        self._props['name'] = name
