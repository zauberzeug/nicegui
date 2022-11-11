from typing import Optional

import justpy as jp

from ..binding import BindableProperty, BindTextMixin
from .group import Group


class Expansion(Group, BindTextMixin):
    text = BindableProperty()

    def __init__(self, text: str, *, icon: Optional[str] = None):
        '''Expansion Element

        Provides an expandable container.

        :param text: title text
        :param icon: optional icon (default: None)
        '''
        view = jp.QExpansionItem(label=text, icon=icon, delete_flag=False, temp=False)
        super().__init__(view)

        self.text = text
        self.bind_text_to(self.view, 'label')

    def set_text(self, text: str):
        self.text = text
