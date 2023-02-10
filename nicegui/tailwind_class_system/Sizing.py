
from typing import Literal

from nicegui.element import Element

Width = Literal[
    'w-0',
    'w-px',
    'w-0.5',
    'w-1',
    'w-1.5',
    'w-2',
    'w-2.5',
    'w-3',
    'w-3.5',
    'w-4',
    'w-5',
    'w-6',
    'w-7',
    'w-8',
    'w-9',
    'w-10',
    'w-11',
    'w-12',
    'w-14',
    'w-16',
    'w-20',
    'w-24',
    'w-28',
    'w-32',
    'w-36',
    'w-40',
    'w-44',
    'w-48',
    'w-52',
    'w-56',
    'w-60',
    'w-64',
    'w-72',
    'w-80',
    'w-96',
    'w-auto',
    'w-1/2',
    'w-1/3',
    'w-2/3',
    'w-1/4',
    'w-2/4',
    'w-3/4',
    'w-1/5',
    'w-2/5',
    'w-3/5',
    'w-4/5',
    'w-1/6',
    'w-2/6',
    'w-3/6',
    'w-4/6',
    'w-5/6',
    'w-1/12',
    'w-2/12',
    'w-3/12',
    'w-4/12',
    'w-5/12',
    'w-6/12',
    'w-7/12',
    'w-8/12',
    'w-9/12',
    'w-10/12',
    'w-11/12',
    'w-full',
    'w-screen',
    'w-min',
    'w-max',
    'w-fit'
]

MinWidth = Literal[
    'min-w-0',
    'min-w-full',
    'min-w-min',
    'min-w-max',
    'min-w-fit'
]

MaxWidth = Literal[
    'max-w-0',
    'max-w-none',
    'max-w-xs',
    'max-w-sm',
    'max-w-md',
    'max-w-lg',
    'max-w-xl',
    'max-w-2xl',
    'max-w-3xl',
    'max-w-4xl',
    'max-w-5xl',
    'max-w-6xl',
    'max-w-7xl',
    'max-w-full',
    'max-w-min',
    'max-w-max',
    'max-w-fit',
    'max-w-prose',
    'max-w-screen-sm',
    'max-w-screen-md',
    'max-w-screen-lg',
    'max-w-screen-xl',
    'max-w-screen-2xl'
]

Height = Literal[
    'h-0',
    'h-px',
    'h-0.5',
    'h-1',
    'h-1.5',
    'h-2',
    'h-2.5',
    'h-3',
    'h-3.5',
    'h-4',
    'h-5',
    'h-6',
    'h-7',
    'h-8',
    'h-9',
    'h-10',
    'h-11',
    'h-12',
    'h-14',
    'h-16',
    'h-20',
    'h-24',
    'h-28',
    'h-32',
    'h-36',
    'h-40',
    'h-44',
    'h-48',
    'h-52',
    'h-56',
    'h-60',
    'h-64',
    'h-72',
    'h-80',
    'h-96',
    'h-auto',
    'h-1/2',
    'h-1/3',
    'h-2/3',
    'h-1/4',
    'h-2/4',
    'h-3/4',
    'h-1/5',
    'h-2/5',
    'h-3/5',
    'h-4/5',
    'h-1/6',
    'h-2/6',
    'h-3/6',
    'h-4/6',
    'h-5/6',
    'h-full',
    'h-screen',
    'h-min',
    'h-max',
    'h-fit'
]

MinHeight = Literal[
    'min-h-0',
    'min-h-full',
    'min-h-screen',
    'min-h-min',
    'min-h-max',
    'min-h-fit'
]

MaxHeight = Literal[
    'max-h-0',
    'max-h-px',
    'max-h-0.5',
    'max-h-1',
    'max-h-1.5',
    'max-h-2',
    'max-h-2.5',
    'max-h-3',
    'max-h-3.5',
    'max-h-4',
    'max-h-5',
    'max-h-6',
    'max-h-7',
    'max-h-8',
    'max-h-9',
    'max-h-10',
    'max-h-11',
    'max-h-12',
    'max-h-14',
    'max-h-16',
    'max-h-20',
    'max-h-24',
    'max-h-28',
    'max-h-32',
    'max-h-36',
    'max-h-40',
    'max-h-44',
    'max-h-48',
    'max-h-52',
    'max-h-56',
    'max-h-60',
    'max-h-64',
    'max-h-72',
    'max-h-80',
    'max-h-96',
    'max-h-none',
    'max-h-full',
    'max-h-screen',
    'max-h-min',
    'max-h-max',
    'max-h-fit'
]


class Sizing:

    def __init__(self, element: Element = Element('')) -> None:
        self.element = element

    def __add(self, _class: str) -> None:
        self.element.classes(add=_class)

    def apply(self, ex_element: Element) -> Element:
        """Apply the Style to an outer element.

        :param ex_element: External Element
        :return: External Element
        """
        return ex_element.classes(add=' '.join(self.element._classes))

    def width(self, _width: Width):
        """Utilities for setting the width of an element."""
        self.__add(_width)
        return self

    def min_width(self, _min_width: MinWidth):
        """Utilities for setting the minimum width of an element."""
        self.__add(_min_width)
        return self

    def max_width(self, _max_width: MaxWidth):
        """Utilities for setting the maximum width of an element."""
        self.__add(_max_width)
        return self

    def height(self, _height: Height):
        """Utilities for setting the height of an element."""
        self.__add(_height)
        return self

    def min_height(self, _min_height: MinHeight):
        """Utilities for setting the minimum height of an element."""
        self.__add(_min_height)
        return self

    def max_height(self, _max_height: MaxHeight):
        """Utilities for setting the maximum height of an element."""
        self.__add(_max_height)
        return self
