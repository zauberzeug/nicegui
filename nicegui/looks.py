from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .element import Element


class Topic():

    def __init__(self, look: Looks):
        self._look = look


class FixedSize(Topic):

    def twelve(self) -> Looks:
        self._look._append_class('w-12')
        return self._look

    def sixty_four(self) -> Looks:
        self._look._append_class('w-64')
        return self._look


class FractionalSize(Topic):

    def one_sixth(self) -> Looks:
        self._look._append_class('w-1/6')
        return self._look


class Width(Topic):

    def full(self) -> Looks:
        self._look._append_class('w-full')
        return self._look

    @property
    def fixed(self) -> FixedSize:
        return FixedSize(self._look)

    @property
    def fractional(self) -> FractionalSize:
        return FractionalSize(self._look)


class Color(Topic):

    def primary(self) -> Looks:
        self._look._append_class('bg-primary')
        return self._look

    def secondary(self) -> Looks:
        self._look._append_class('bg-secondary')
        return self._look

    def teal(self, level: float) -> Looks:
        level = int(level * 10)
        self._look._append_class(f'bg-teal-{level}')
        return self._look


class Spacing(Topic):

    def __init__(self, look: Looks, prefix: str):
        super().__init__(look)
        self.prefix = prefix

    def small(self) -> Looks:
        self._look._append_class(f'{self.prefix}-sm')
        return self._look


class Padding(Topic):

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._look, 'q-py')


class MainAxis(Topic):

    def start(self) -> Looks:
        self._look._append_class('justify-start')
        return self._look

    def end(self) -> Looks:
        self._look._append_class('justify-end')
        return self._look

    def center(self) -> Looks:
        self._look._append_class('justify-center')
        return self._look


class Text(Topic):

    def red(self, level: float) -> Looks:
        level = int(level * 1000)
        self._look._append_class(f'text-red-{level}')
        return self._look

    def gray(self, level: float) -> Looks:
        self._look._append_class(f'text-red-{level}')
        return self._look


class Alignment(Topic):

    @property
    def main_axis(self) -> MainAxis:
        return MainAxis(self._look)


class Looks:

    def __init__(self, element: Optional['Element'] = None):
        self.classes: List[str] = []
        self.element = element
        self.configure_hover = False

    def _append_class(self, name: str):
        if self.configure_hover:
            name = f'hover:{name}'
        self.classes.append(name)

    @property
    def width(self) -> Width:
        '''Width'''
        return Width(self)

    @property
    def background(self) -> Color:
        '''Background'''
        return Color(self)

    @property
    def padding(self) -> Padding:
        '''Padding'''
        return Padding(self)

    @property
    def align(self) -> Alignment:
        '''Alignment'''
        return Alignment(self)

    @property
    def text(self) -> Text:
        '''Text'''
        return Text(self)

    def on_hover(self) -> Looks:
        self.configure_hover = True
        return self

    def extend(self, other: Looks) -> Looks:
        self.classes.extend(other.classes)
        return self
