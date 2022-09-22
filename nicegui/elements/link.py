from typing import Callable, Union

import justpy as jp

from .. import globals
from .group import Group


class Link(Group):

    def __init__(self, text: str = '', target: Union[Callable, str] = '#'):
        """Link

        Create a hyperlink.

        :param text: display text
        :param target: page function or string that is a an absolute URL or relative path from base URL
        """
        href = target if isinstance(target, str) else globals.find_route(target)[1:]
        view = jp.A(text=text, href=href, classes='underline text-blue', temp=False)

        super().__init__(view)
