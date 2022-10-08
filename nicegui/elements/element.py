from __future__ import annotations

import shlex
from typing import Dict, Optional

import justpy as jp

from .. import globals
from ..binding import BindableProperty, BindVisibilityMixin
from ..page import Page, find_parent_view
from ..task_logger import create_task


def _handle_visibility_change(sender: Element, visible: bool) -> None:
    (sender.view.remove_class if visible else sender.view.set_class)('hidden')
    sender.update()


class Element(BindVisibilityMixin):
    visible = BindableProperty(on_change=_handle_visibility_change)

    def __init__(self, view: jp.HTMLBaseComponent):
        self.parent_view = find_parent_view()
        self.parent_view.add(view)
        self.view = view
        assert len(self.parent_view.pages) == 1
        self.page: Page = list(self.parent_view.pages.values())[0]
        self.view.add_page(self.page)

        self.visible = True

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None):
        '''HTML classes to modify the look of the element.
        Every class in the `remove` parameter will be removed from the element.
        Classes are separated with a blank space.
        This can be helpful if the predefined classes by NiceGUI are not wanted in a particular styling.
        '''
        class_list = self.view.classes.split() if replace is None else []
        class_list = [c for c in class_list if c not in (remove or '').split()]
        class_list += (add or '').split()
        class_list += (replace or '').split()
        new_classes = ' '.join(dict.fromkeys(class_list))  # NOTE: remove duplicates while preserving order
        if self.view.classes != new_classes:
            self.view.classes = new_classes
            self.update()
        return self

    @staticmethod
    def _parse_style(text: Optional[str]) -> Dict[str, str]:
        return dict((word.strip() for word in part.split(':')) for part in text.strip('; ').split(';')) if text else {}

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None):
        '''CSS style sheet definitions to modify the look of the element.
        Every style in the `remove` parameter will be removed from the element.
        Styles are separated with a semicolon.
        This can be helpful if the predefined style sheet definitions by NiceGUI are not wanted in a particular styling.
        '''
        style_dict = self._parse_style((self.view.style or '').strip('; ')) if replace is None else {}
        for key in self._parse_style(remove):
            del style_dict[key]
        style_dict.update(self._parse_style(add))
        style_dict.update(self._parse_style(replace))
        new_style = ';'.join(f'{key}:{value}' for key, value in style_dict.items())
        if self.view.style != new_style:
            self.view.style = new_style
            self.update()
        return self

    @staticmethod
    def _parse_props(text: Optional[str]) -> Dict[str, str]:
        if not text:
            return {}
        lexer = shlex.shlex(text, posix=True)
        lexer.whitespace = ' '
        lexer.wordchars += '=-.%'
        return dict(word.split('=', 1) if '=' in word else (word, True) for word in lexer)

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None):
        '''Quasar props https://quasar.dev/vue-components/button#design to modify the look of the element.
        Boolean props will automatically activated if they appear in the list of the `add` property.
        Props are separated with a blank space. String values must be quoted.
        Every prop passed to the `remove` parameter will be removed from the element.
        This can be helpful if the predefined props by NiceGUI are not wanted in a particular styling.
        '''
        needs_update = False
        for key in self._parse_props(remove):
            if getattr(self.view, key, None) is not None:
                needs_update = True
            setattr(self.view, key, None)
        for key, value in self._parse_props(add).items():
            if getattr(self.view, key, None) != value:
                needs_update = True
            setattr(self.view, key, value)
        if needs_update:
            self.update()
        return self

    def tooltip(self, text: str, *, props: str = ''):
        tooltip = jp.QTooltip(text=text, temp=False)
        for prop in props.split():
            if '=' in prop:
                setattr(tooltip, *prop.split('='))
            else:
                setattr(tooltip, prop, True)
        tooltip.add_page(self.page)
        self.view.add(tooltip)
        self.update()
        return self

    def update(self) -> None:
        if globals.loop is not None:
            create_task(self.view.update())
