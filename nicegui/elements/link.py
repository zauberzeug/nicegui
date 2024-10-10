from typing import Any, Callable, Union

from ..client import Client
from ..element import Element
from .mixins.text_element import TextElement


class Link(TextElement, component='link.js', default_classes='nicegui-link'):

    def __init__(self,
                 text: str = '',
                 target: Union[Callable[..., Any], str, Element] = '#',
                 new_tab: bool = False,
                 ) -> None:
        """Link

        Create a hyperlink.

        To jump to a specific location within a page you can place linkable anchors with `ui.link_target("name")`
        and link to it with `ui.link(target="#name")`.

        :param text: display text
        :param target: page function, NiceGUI element on the same page or string that is a an absolute URL or relative path from base URL
        :param new_tab: open link in new tab (default: False)
        """
        super().__init__(text=text)
        if isinstance(target, str):
            self._props['href'] = target
        elif isinstance(target, Element):
            self._props['href'] = f'#c{target.id}'
        elif callable(target):
            self._props['href'] = Client.page_routes[target]
        self._props['target'] = '_blank' if new_tab else '_self'


class LinkTarget(Element):

    def __init__(self, name: str) -> None:
        """Link target

        Create an anchor tag that can be used as inner-page target for links.

        :param name: target name
        """
        super().__init__('a')
        self._props['name'] = name
