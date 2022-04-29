from typing import Union

import justpy as jp

from .group import Group
from .page import Page


class Link(Group):

    def __init__(self, text: str = '', target: Union[Page, str] = '#'):
        """Link

        Create a hyperlink.

        :param text: display text
        :param target: page or string that is a an absolute URL or relative path from base URL
        """
        href = target if isinstance(target, str) else target.route[1:]
        view = jp.A(text=text, href=href, classes='underline text-blue', temp=False)

        super().__init__(view)
