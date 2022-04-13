from typing import Optional

import justpy as jp

from .group import Group


class Expansion(Group):

    def __init__(self, text: str, *, icon: Optional[str] = None):
        '''Expansion Element

        Provides an expandable container.

        :param text: title text
        :param icon: optional icon (default: None)
        '''
        view = jp.QExpansionItem(label=text, icon=icon, delete_flag=False, temp=False)
        super().__init__(view)
