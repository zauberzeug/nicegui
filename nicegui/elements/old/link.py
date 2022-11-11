from typing import Callable, Union

import justpy as jp

from .. import globals
from .element import Element
from .group import Group


class Link(Group):

    def __init__(self, text: str = '', target: Union[Callable, str] = '#'):
        """Link

        Create a hyperlink.

        To jump to a specific location within a page you can place linkable anchors with `ui.link_target("name")`
        and link to it with `ui.link(target="#name")`.

        :param text: display text
        :param target: page function or string that is a an absolute URL or relative path from base URL
        """
        href = target if isinstance(target, str) else globals.find_route(target)[1:]
        view = jp.A(text=text, href=href, classes='underline text-blue', temp=False)

        super().__init__(view)


class LinkTarget(Element):

    def __init__(self, name: str) -> None:
        """Link target

        Create an anchor tag that can be used as inner-page target for links.

        :param name: target name
        """
        view = jp.A(name=name, temp=False)
        super().__init__(view)
