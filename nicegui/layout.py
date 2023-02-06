from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional

from .element import Element

ElementSize = Literal[None, '0', '0.5', '1', '1.5', '6', '12', '64', '1/2', '1/6', '2/3', 'full']
MainAxisChildAlignment = Literal[None, 'start', 'center', 'end', 'evenly', 'between', 'around']
CrossAxisChildAlignment = Literal[None, 'start', 'center', 'end', 'stretch', 'baseline']


class Topic():

    def __init__(self, looks: Layout, prefix: str = '', prop: str = None):
        self._looks: Layout = looks
        self._prefix: str = prefix
        self._prop: Optional[str] = prop


class Color(Topic):

    def _apply(self, color: str) -> Layout:
        if self._prop:
            self._looks._props[self._prop] = color
        else:
            self._looks._classes.append(f'{self._prefix}-{color}')
        return self._looks

    def primary(self) -> Layout:
        self._apply('primary')
        return self._looks

    def secondary(self) -> Layout:
        self._apply('secondary')
        return self._looks

    def teal(self, level: float) -> Layout:
        level = int(level * 10)
        self._apply(f'teal-{level}')
        return self._looks

    def grey(self, level: float) -> Layout:
        level = int(level * 10)
        self._apply(f'grey-{level}')
        return self._looks

    def yellow(self, level: float) -> Layout:
        level = int(level * 10)
        self._apply(f'yellow-{level}')
        return self._looks


class Shadow(Topic):

    def small(self) -> Layout:
        self._looks._classes.append('shadow-4')
        return self._looks


class Spacing(Topic):

    def __init__(self, look: Layout, prefix: str):
        super().__init__(look)
        self.prefix = prefix

    def small(self) -> Layout:
        self._looks._classes.append(f'{self.prefix}-sm')
        return self._looks

    def auto(self) -> Layout:
        if self.prefix[-2] != 'm':
            raise ValueError('auto spacing can only be used on margins')
        if not any(self.prefix.endswith(direction) for direction in ['l', 'r', 'x']):
            raise ValueError('auto spacing can only be used on x axis')
        self._looks._classes.append(f'{self.prefix}-auto')
        return self._looks


class Padding(Topic):

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._looks, 'q-py')


class Margin(Topic):

    @property
    def x_axis(self) -> Spacing:
        return Spacing(self._looks, 'q-mx')

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._looks, 'q-my')

    @property
    def all(self) -> Spacing:
        return Spacing(self._looks, 'q-ma')

    @property
    def left(self) -> Spacing:
        return Spacing(self._looks, 'q-ml')


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

    def children(self, main_axis: MainAxisChildAlignment = None, cross_axis: CrossAxisChildAlignment = None) -> Layout:
        '''configure alignment'''
        if main_axis is not None:
            self._looks._classes.append(f'justify-{main_axis}')
        if cross_axis is not None:
            self._looks._classes.append(f'items-{cross_axis}')
        return self._looks

    @property
    def center(self) -> Layout:
        self._looks.margin.x_axis.auto()
        return self._looks


@dataclass
class Bindable:
    opacity: float = 1.0


class Layout:

    def __init__(self, element=None):
        self.element: Optional[Element] = element
        self._classes: List[str] = []
        self._props: Dict[str, Any] = {}
        self.bindables = Bindable()

    def size(self, width: ElementSize = None, height: ElementSize = None) -> Layout:
        '''Set the dimensions of the element'''
        if width is not None:
            self._classes.append(f'w-{width}')
        if height is not None:
            self._classes.append(f'h-{height}')
        return self

    @property
    def background(self) -> Color:
        '''Background'''
        return Color(self, 'bg')

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

    @property
    def margin(self) -> Margin:
        '''Margin'''
        return Margin(self)

    @property
    def shadow(self) -> Shadow:
        '''Shadow'''
        return Shadow(self)

    def row(self) -> Layout:
        self._classes.append('row')
        self.align.children(main_axis='start').gap.medium()
        return self

    def on_hover(self, looks: Layout) -> Layout:
        self._classes.extend([f'hover:{c}' for c in looks._classes])
        return self

    def add(self, other: Layout) -> Layout:
        self._classes.extend(other._classes)
        self._props.update(other._props)
        return self

    def opacity(self, opacity: float) -> Layout:
        self.bindables.opacity = opacity
        return self

    def __enter__(self):
        if self.element is None:
            self.element = Element('div')
            self.element.layout = self
        self.element.__enter__()

    def __exit__(self, *_):
        self.element.__exit__(*_)
        self.element = None

    def __call__(self, *args: Any, **kwds: Any) -> 'Layout':
        return deepcopy(self)


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


class IconSizing(Topic):

    def small(self) -> Layout:
        self._looks._props['size'] = '1rem'
        return self._looks

    def medium(self) -> Layout:
        self._looks._props['size'] = '3rem'
        return self._looks

    def large(self) -> Layout:
        self._looks._props['size'] = '5rem'
        return self._looks


class IconLayout(Layout):

    @property
    def size(self) -> IconSizing:
        return IconSizing(self)

    @property
    def color(self) -> Color:
        return Color(self, prop='color')


layout = Layout()
