from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, overload

from .element import Element

ElementSize = Literal[None, '0', '0.5', '1', '1.5', '6', '12', '64', '1/2', '1/6', '2/3', 'full']
Color = Literal[None, 'primary', 'secondary', 'teal', 'grey', 'yellow']
Tone = Literal[None, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ThemeColor = Literal[None, 'primary', 'secondary', 'accent', 'positive', 'negative', 'info', 'warning']


class Topic():

    def __init__(self, looks: Layout, prefix: str = '', prop: str = None):
        self._looks: Layout = looks
        self._prefix: str = prefix
        self._prop: Optional[str] = prop


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

    ChildrenOnMainAxis = Literal[None, 'start', 'center', 'end', 'evenly', 'between', 'around']
    ChildrenOnCrossAxis = Literal[None, 'start', 'center', 'end', 'stretch', 'baseline']

    def children(self, main_axis: ChildrenOnMainAxis = None, cross_axis: ChildrenOnCrossAxis = None) -> Layout:
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

    @overload
    def background(self, theme_color: ThemeColor) -> Layout:
        '''Use one of the theme colors which can be defined with `ui.color`'''

    @overload
    def background(self, color: Color, tone: Tone) -> Layout:
        '''Pick a color and optional tone to specify the shade'''

    def background(self, theme_color: ThemeColor = ..., color: Color = ...,  tone: Tone = ...) -> Layout:
        if theme_color is not ...:
            self._classes.append(f'bg-{theme_color}')
        elif color is not ...:
            if tone is ...:
                self._classes.append(f'bg-{color}')
            self._classes.append(f'bg-{color}-{tone}')
        return self

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

    @overload
    def color(self, theme_color: ThemeColor) -> IconLayout:
        '''Use one of the theme colors which can be defined with `ui.color`'''

    @overload
    def color(self, color: Color, tone: Tone) -> IconLayout:
        '''Pick a color by name and optional a tone to specify the shade'''

    def color(self, theme_color: ThemeColor = ..., color: Color = ...,  tone: Tone = ...) -> IconLayout:
        '''Set the color of the icon'''
        if theme_color is not ...:
            self._props['color'] = theme_color
        elif color is not ...:
            if tone is ...:
                self._props['color'] = f'bg-{color}'
            self._props['color'] = f'bg-{color}-{tone}'
        return self


layout = Layout()
