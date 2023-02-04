from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .element import Element


class Topic():

    def __init__(self, looks: Layout, prefix: str = ''):
        self._looks = looks
        self._prefix = prefix


class FixedSize(Topic):

    def twelve(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-12')
        return self._looks

    def twenty(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-20')
        return self._looks

    def forty_eight(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-48')
        return self._looks

    def sixty_four(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-64')
        return self._looks


class FractionalSize(Topic):

    def one_sixth(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-1/6')
        return self._looks

    def two_thirds(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-2/3')
        return self._looks

    def one_half(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-1/2')
        return self._looks


class Sizing(Topic):

    def full(self) -> Layout:
        self._looks._classes.append(f'{self._prefix}-full')
        return self._looks

    @property
    def fixed(self) -> FixedSize:
        return FixedSize(self._looks, self._prefix)

    @property
    def fractional(self) -> FractionalSize:
        return FractionalSize(self._looks, self._prefix)


class Color(Topic):

    def primary(self) -> Layout:
        self._looks._classes.append('bg-primary')
        return self._looks

    def secondary(self) -> Layout:
        self._looks._classes.append('bg-secondary')
        return self._looks

    def teal(self, level: float) -> Layout:
        level = int(level * 10)
        self._looks._classes.append(f'bg-teal-{level}')
        return self._looks

    def grey(self, level: float) -> Layout:
        level = int(level * 10)
        self._looks._classes.append(f'bg-grey-{level}')
        return self._looks


class Spacing(Topic):

    def __init__(self, look: Layout, prefix: str):
        super().__init__(look)
        self.prefix = prefix

    def small(self) -> Layout:
        self._looks._classes.append(f'{self.prefix}-sm')
        return self._looks


class Padding(Topic):

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._looks, 'q-py')


class MainAxis(Topic):

    def start(self) -> Layout:
        self._looks._classes.append('justify-start')
        return self._looks

    def end(self) -> Layout:
        self._looks._classes.append('justify-end')
        return self._looks

    def center(self) -> Layout:
        self._looks._classes.append('justify-center')
        return self._looks

    def evenly(self) -> Layout:
        self._looks._classes.append('justify-evenly')
        return self._looks


class CrossAxis(Topic):

    def start(self) -> Layout:
        self._looks._classes.append('items-start')
        return self._looks

    def center(self) -> Layout:
        self._looks._classes.append('items-center')
        return self._looks


class Text(Topic):

    def red(self, level: float) -> Layout:
        level = int(level * 1000)
        self._looks._classes.append(f'text-red-{level}')
        return self._looks

    def gray(self, level: float) -> Layout:
        self._looks._classes.append(f'text-red-{level}')
        return self._looks


class Gap(Topic):

    def none(self) -> Layout:
        self._looks._classes.append('gap-0')
        return self._looks

    def small(self) -> Layout:
        self._looks._classes.append('gap-2')
        return self._looks

    def medium(self) -> Layout:
        self._looks._classes.append('gap-4')
        return self._looks


class Alignment(Topic):

    @property
    def main_axis(self) -> MainAxis:
        return MainAxis(self._looks)

    @property
    def cross_axis(self) -> CrossAxis:
        return CrossAxis(self._looks)


class Layout:

    def __init__(self, element: Optional['Element'] = None):
        self.element = element
        self._classes: List[str] = []
        self._props: Dict[str, Any] = {}

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

    @property
    def gap(self) -> Gap:
        '''Gap'''
        return Gap(self)

    def on_hover(self, looks: Layout) -> Layout:
        self._classes.extend([f'hover:{c}' for c in looks._classes])
        return self

    def add(self, other: Layout) -> Layout:
        self._classes.extend(other._classes)
        self._props.update(other._props)
        return self


class ButtonLayout(Layout):

    def rounded(self) -> Layout:
        self._props['rounded'] = True
        return self

    def square(self) -> Layout:
        self._props['square'] = True
        return self

    def flat(self) -> Layout:
        self._props['flat'] = True
        return self

    def outline(self) -> Layout:
        self._props['outline'] = True
        return self

    def unelevated(self) -> Layout:
        self._props['unelevated'] = True
        return self
