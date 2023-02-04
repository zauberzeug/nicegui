from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .element import Element


class Topic():

    def __init__(self, looks: Looks, prefix: str = ''):
        self._looks = looks
        self._prefix = prefix


class FixedSize(Topic):

    def twelve(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-12')
        return self._looks

    def twenty(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-20')
        return self._looks

    def forty_eight(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-48')
        return self._looks

    def sixty_four(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-64')
        return self._looks


class FractionalSize(Topic):

    def one_sixth(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-1/6')
        return self._looks

    def two_thirds(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-2/3')
        return self._looks


class Sizing(Topic):

    def full(self) -> Looks:
        self._looks.classes.append(f'{self._prefix}-full')
        return self._looks

    @property
    def fixed(self) -> FixedSize:
        return FixedSize(self._looks, self._prefix)

    @property
    def fractional(self) -> FractionalSize:
        return FractionalSize(self._looks, self._prefix)


class Color(Topic):

    def primary(self) -> Looks:
        self._looks.classes.append('bg-primary')
        return self._looks

    def secondary(self) -> Looks:
        self._looks.classes.append('bg-secondary')
        return self._looks

    def teal(self, level: float) -> Looks:
        level = int(level * 10)
        self._looks.classes.append(f'bg-teal-{level}')
        return self._looks

    def grey(self, level: float) -> Looks:
        level = int(level * 10)
        self._looks.classes.append(f'bg-grey-{level}')
        return self._looks


class Spacing(Topic):

    def __init__(self, look: Looks, prefix: str):
        super().__init__(look)
        self.prefix = prefix

    def small(self) -> Looks:
        self._looks.classes.append(f'{self.prefix}-sm')
        return self._looks


class Padding(Topic):

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._looks, 'q-py')


class MainAxis(Topic):

    def start(self) -> Looks:
        self._looks.classes.append('justify-start')
        return self._looks

    def end(self) -> Looks:
        self._looks.classes.append('justify-end')
        return self._looks

    def center(self) -> Looks:
        self._looks.classes.append('justify-center')
        return self._looks

    def evenly(self) -> Looks:
        self._looks.classes.append('justify-evenly')
        return self._looks


class CrossAxis(Topic):

    def start(self) -> Looks:
        self._looks.classes.append('items-start')
        return self._looks

    def center(self) -> Looks:
        self._looks.classes.append('items-center')
        return self._looks


class Text(Topic):

    def red(self, level: float) -> Looks:
        level = int(level * 1000)
        self._looks.classes.append(f'text-red-{level}')
        return self._looks

    def gray(self, level: float) -> Looks:
        self._looks.classes.append(f'text-red-{level}')
        return self._looks


class Alignment(Topic):

    @property
    def main_axis(self) -> MainAxis:
        return MainAxis(self._looks)

    @property
    def cross_axis(self) -> CrossAxis:
        return CrossAxis(self._looks)


class Looks:

    def __init__(self, element: Optional['Element'] = None):
        self.classes: List[str] = []
        self.element = element

    @property
    def width(self) -> Sizing:
        '''Width'''
        return Sizing(self, 'w')

    @property
    def height(self) -> Sizing:
        '''Height'''
        return Sizing(self, 'h')

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

    def on_hover(self, looks: Looks) -> Looks:
        self.classes.extend([f'hover:{c}' for c in looks.classes])
        return self

    def extend(self, other: Looks) -> Looks:
        self.classes.extend(other.classes)
        return self
