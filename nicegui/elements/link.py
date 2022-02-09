from typing import Union
import justpy as jp
from .element import Element
from .page import Page

class Link(Element):

    def __init__(self,
                 text: str = '',
                 target: Union[Page, str] = '#',
                 ):
        """Link

        Create a link.

        :param text: link text
        :param target: link target (either a string or a page object)
        """
        href = target if isinstance(target, str) else target.route
        view = jp.A(text=text, href=href, classes='underline text-blue')

        super().__init__(view)
