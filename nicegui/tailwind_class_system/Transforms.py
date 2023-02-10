
from typing import Literal

from nicegui.element import Element

Scale = Literal[
    'scale-0',
    'scale-x-0',
    'scale-y-0',
    'scale-50',
    'scale-x-50',
    'scale-y-50',
    'scale-75',
    'scale-x-75',
    'scale-y-75',
    'scale-90',
    'scale-x-90',
    'scale-y-90',
    'scale-95',
    'scale-x-95',
    'scale-y-95',
    'scale-100',
    'scale-x-100',
    'scale-y-100',
    'scale-105',
    'scale-x-105',
    'scale-y-105',
    'scale-110',
    'scale-x-110',
    'scale-y-110',
    'scale-125',
    'scale-x-125',
    'scale-y-125',
    'scale-150',
    'scale-x-150',
    'scale-y-150'
]

Rotate = Literal[
    'rotate-0',
    'rotate-1',
    'rotate-2',
    'rotate-3',
    'rotate-6',
    'rotate-12',
    'rotate-45',
    'rotate-90',
    'rotate-180'
]

Translate = Literal[
    'translate-x-0',
    'translate-y-0',
    'translate-x-px',
    'translate-y-px',
    'translate-x-0.5',
    'translate-y-0.5',
    'translate-x-1',
    'translate-y-1',
    'translate-x-1.5',
    'translate-y-1.5',
    'translate-x-2',
    'translate-y-2',
    'translate-x-2.5',
    'translate-y-2.5',
    'translate-x-3',
    'translate-y-3',
    'translate-x-3.5',
    'translate-y-3.5',
    'translate-x-4',
    'translate-y-4',
    'translate-x-5',
    'translate-y-5',
    'translate-x-6',
    'translate-y-6',
    'translate-x-7',
    'translate-y-7',
    'translate-x-8',
    'translate-y-8',
    'translate-x-9',
    'translate-y-9',
    'translate-x-10',
    'translate-y-10',
    'translate-x-11',
    'translate-y-11',
    'translate-x-12',
    'translate-y-12',
    'translate-x-14',
    'translate-y-14',
    'translate-x-16',
    'translate-y-16',
    'translate-x-20',
    'translate-y-20',
    'translate-x-24',
    'translate-y-24',
    'translate-x-28',
    'translate-y-28',
    'translate-x-32',
    'translate-y-32',
    'translate-x-36',
    'translate-y-36',
    'translate-x-40',
    'translate-y-40',
    'translate-x-44',
    'translate-y-44',
    'translate-x-48',
    'translate-y-48',
    'translate-x-52',
    'translate-y-52',
    'translate-x-56',
    'translate-y-56',
    'translate-x-60',
    'translate-y-60',
    'translate-x-64',
    'translate-y-64',
    'translate-x-72',
    'translate-y-72',
    'translate-x-80',
    'translate-y-80',
    'translate-x-96',
    'translate-y-96',
    'translate-x-1/2',
    'translate-x-1/3',
    'translate-x-2/3',
    'translate-x-1/4',
    'translate-x-2/4',
    'translate-x-3/4',
    'translate-x-full',
    'translate-y-1/2',
    'translate-y-1/3',
    'translate-y-2/3',
    'translate-y-1/4',
    'translate-y-2/4',
    'translate-y-3/4',
    'translate-y-full'
]

Skew = Literal[
    'skew-x-0',
    'skew-y-0',
    'skew-x-1',
    'skew-y-1',
    'skew-x-2',
    'skew-y-2',
    'skew-x-3',
    'skew-y-3',
    'skew-x-6',
    'skew-y-6',
    'skew-x-12',
    'skew-y-12'
]

TransformOrigin = Literal[
    'origin-center',
    'origin-top',
    'origin-top-right',
    'origin-right',
    'origin-bottom-right',
    'origin-bottom',
    'origin-bottom-left',
    'origin-left',
    'origin-top-left'
]


class Transforms:

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

    def scale(self, _scale: Scale):
        """Utilities for scaling elements with transform."""
        self.__add(_scale)
        return self

    def rotate(self, _rotate: Rotate):
        """Utilities for rotating elements with transform."""
        self.__add(_rotate)
        return self

    def translate(self, _translate: Translate):
        """Utilities for translating elements with transform."""
        self.__add(_translate)
        return self

    def skew(self, _skew: Skew):
        """Utilities for skewing elements with transform."""
        self.__add(_skew)
        return self

    def transform_origin(self, _transform_origin: TransformOrigin):
        """Utilities for specifying the origin for an element's transformations."""
        self.__add(_transform_origin)
        return self
