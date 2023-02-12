from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, overload

from typing_extensions import Literal

from .element import Element

ElementSize = Literal[None, '0', '0.5', '1', '1.5', '6', '12', '64', '1/2', '1/6', '2/3', 'full']
Color = Literal[None, 'teal', 'grey', 'yellow', 'orange']
Tone = Literal[None, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ThemeColor = Literal[None, 'primary', 'secondary', 'accent', 'positive', 'negative', 'info', 'warning']


class Topic():

    def __init__(self, layout: Layout, prefix: str = '', prop: str = None):
        self._layout: Layout = layout
        self._prefix: str = prefix
        self._prop: Optional[str] = prop


class Shadow(Topic):

    def small(self) -> Layout:
        self._layout._classes.append('shadow-4')
        return self._layout


class Spacing(Topic):

    def __init__(self, look: Layout, prefix: str):
        super().__init__(look)
        self.prefix = prefix

    def small(self) -> Layout:
        self._layout._classes.append(f'{self.prefix}-sm')
        return self._layout

    def auto(self) -> Layout:
        if self.prefix[-2] != 'm':
            raise ValueError('auto spacing can only be used on margins')
        if not any(self.prefix.endswith(direction) for direction in ['l', 'r', 'x']):
            raise ValueError('auto spacing can only be used on x axis')
        self._layout._classes.append(f'{self.prefix}-auto')
        return self._layout


class Padding(Topic):

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._layout, 'q-py')

    @property
    def all(self) -> Spacing:
        return Spacing(self._layout, 'q-pa')


class Margin(Topic):

    @property
    def x_axis(self) -> Spacing:
        return Spacing(self._layout, 'q-mx')

    @property
    def y_axis(self) -> Spacing:
        return Spacing(self._layout, 'q-my')

    @property
    def all(self) -> Spacing:
        return Spacing(self._layout, 'q-ma')

    @property
    def left(self) -> Spacing:
        return Spacing(self._layout, 'q-ml')


class Text(Topic):

    def red(self, level: float) -> Layout:
        level = int(level * 1000)
        self._layout._classes.append(f'text-red-{level}')
        return self._layout

    def gray(self, level: float) -> Layout:
        self._layout._classes.append(f'text-red-{level}')
        return self._layout


class Gap(Topic):

    def none(self) -> Layout:
        self._layout._classes.append('gap-0')
        return self._layout

    def small(self) -> Layout:
        self._layout._classes.append('gap-2')
        return self._layout

    def medium(self) -> Layout:
        self._layout._classes.append('gap-4')
        return self._layout

    def large(self) -> Layout:
        self._layout._classes.append('gap-6')
        return self._layout


class Alignment(Topic):

    ChildrenOnMainAxis = Literal[None, 'start', 'center', 'end', 'evenly', 'between', 'around']
    ChildrenOnCrossAxis = Literal[None, 'start', 'center', 'end', 'stretch', 'baseline']

    def children(self, main_axis: ChildrenOnMainAxis = None, cross_axis: ChildrenOnCrossAxis = None) -> Layout:
        '''configure alignment'''
        if main_axis is not None:
            self._layout._classes.append(f'justify-{main_axis}')
        if cross_axis is not None:
            self._layout._classes.append(f'items-{cross_axis}')
        return self._layout

    def center(self) -> Layout:
        self._layout.margin.x_axis.auto()
        return self._layout


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

    def background(self, color: Color,  tone: Tone = None) -> Layout:
        self._classes.append(f'bg-{color}' if tone is None else f'bg-{color}-{tone}')
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
        self._classes.append('flex flex-row')
        self.align.children(main_axis='start').gap.medium()
        return self

    def on_hover(self, layout: Layout) -> Layout:
        self._classes.extend([f'hover:{c}' for c in layout._classes])
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

    def copy(self) -> 'Layout':
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

    def small(self) -> 'IconLayout':
        self._layout._props['size'] = '1rem'
        return self._layout

    def medium(self) -> 'IconLayout':
        self._layout._props['size'] = '3rem'
        return self._layout

    def large(self) -> 'IconLayout':
        self._layout._props['size'] = '5rem'
        return self._layout


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

    def color(self, color: str,  tone: Tone = None) -> IconLayout:
        '''Set the color of the icon'''
        self._props['color'] = color if tone is None else f'{color}-{tone}'
        return self


Direction = Literal['horizontal', 'vertical']


def layout(flow: Direction = 'vertical', subdivision: Optional[int] = None) -> Layout:
    '''Create a layout

    :param flow: specify if child elements should be arranged 'horizontal' or 'vertical' (default: 'vertical')
    :param subdivision: specify if the flow of elements should be divided into rows/columns (default: None, which means flex placement)
    '''
    l = Layout()
    if flow is not None:
        l.gap.small()
        if subdivision is None:
            if flow is 'horizontal':
                l._classes.append('flex flex-row')
            elif flow is 'vertical':
                l._classes.append('flex flex-col')
        else:
            if flow is 'horizontal':
                l._classes.append(f'grid grid-cols-{subdivision} grid-flow-row')
            elif flow is 'vertical':
                l._classes.append(f'grid grid-rows-{subdivision} grid-flow-col')
    return l
