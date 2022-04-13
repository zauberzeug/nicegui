from typing import Optional

import justpy as jp

from ..binding import BindableProperty, bind_from, bind_to
from .group import Group


class Expansion(Group):
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

    def bind_text_to(self, target_object, target_name, forward=lambda x: x):
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self

    def bind_text_from(self, target_object, target_name, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        return self

    def bind_text(self, target_object, target_name, forward=lambda x: x, backward=lambda x: x):
        bind_from(self, 'text', target_object, target_name, backward=backward)
        bind_to(self, 'text', target_object, target_name, forward=forward)
        return self
