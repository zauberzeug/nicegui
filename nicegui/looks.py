from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .element import Element


class Topic():

    def __init__(self, look: Looks):
        self._look = look


class Width(Topic):

    def full(self) -> Looks:
        self._look.classes.append('w-full')
        return self._look


class Color(Topic):

    def primary(self) -> Looks:
        self._look.classes.append('bg-primary')
        return self._look


class Padding(Topic):

    def two(self) -> Looks:
        self._look.classes.append('p-2')
        return self._look


class MainAxis(Topic):

    def start(self) -> Looks:
        self._look.classes.append('justify-start')
        return self._look

    def end(self) -> Looks:
        self._look.classes.append('justify-end')
        return self._look

    def center(self) -> Looks:
        self._look.classes.append('justify-center')
        return self._look


class Alignment(Topic):

    @property
    def main_axis(self) -> MainAxis:
        return MainAxis(self._look)


class Looks:

    def __init__(self, element: Optional['Element'] = None):
        self.classes: List[str] = []
        self.element = element

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
