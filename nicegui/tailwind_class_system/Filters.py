
from typing import Literal

from nicegui.element import Element

Blur = Literal[
    'blur-none',
    'blur-sm',
    'blur',
    'blur-md',
    'blur-lg',
    'blur-xl',
    'blur-2xl',
    'blur-3xl'
]

Brightness = Literal[
    'brightness-0',
    'brightness-50',
    'brightness-75',
    'brightness-90',
    'brightness-95',
    'brightness-100',
    'brightness-105',
    'brightness-110',
    'brightness-125',
    'brightness-150',
    'brightness-200'
]

Contrast = Literal[
    'contrast-0',
    'contrast-50',
    'contrast-75',
    'contrast-100',
    'contrast-125',
    'contrast-150',
    'contrast-200'
]

DropShadow = Literal[
    'drop-shadow-sm',
    'drop-shadow',
    'drop-shadow-md',
    'drop-shadow-lg',
    'drop-shadow-xl',
    'drop-shadow-2xl',
    'drop-shadow-none'
]

Grayscale = Literal[
    'grayscale-0',
    'grayscale'
]

HueRotate = Literal[
    'hue-rotate-0',
    'hue-rotate-15',
    'hue-rotate-30',
    'hue-rotate-60',
    'hue-rotate-90',
    'hue-rotate-180'
]

Invert = Literal[
    'invert-0',
    'invert'
]

Saturate = Literal[
    'saturate-0',
    'saturate-50',
    'saturate-100',
    'saturate-150',
    'saturate-200'
]

Sepia = Literal[
    'sepia-0',
    'sepia'
]

BackdropBlur = Literal[
    'backdrop-blur-none',
    'backdrop-blur-sm',
    'backdrop-blur',
    'backdrop-blur-md',
    'backdrop-blur-lg',
    'backdrop-blur-xl',
    'backdrop-blur-2xl',
    'backdrop-blur-3xl'
]

BackdropBrightness = Literal[
    'backdrop-brightness-0',
    'backdrop-brightness-50',
    'backdrop-brightness-75',
    'backdrop-brightness-90',
    'backdrop-brightness-95',
    'backdrop-brightness-100',
    'backdrop-brightness-105',
    'backdrop-brightness-110',
    'backdrop-brightness-125',
    'backdrop-brightness-150',
    'backdrop-brightness-200'
]

BackdropContrast = Literal[
    'backdrop-contrast-0',
    'backdrop-contrast-50',
    'backdrop-contrast-75',
    'backdrop-contrast-100',
    'backdrop-contrast-125',
    'backdrop-contrast-150',
    'backdrop-contrast-200'
]

BackdropGrayscale = Literal[
    'backdrop-grayscale-0',
    'backdrop-grayscale'
]

BackdropHueRotate = Literal[
    'backdrop-hue-rotate-0',
    'backdrop-hue-rotate-15',
    'backdrop-hue-rotate-30',
    'backdrop-hue-rotate-60',
    'backdrop-hue-rotate-90',
    'backdrop-hue-rotate-180'
]

BackdropInvert = Literal[
    'backdrop-invert-0',
    'backdrop-invert'
]

BackdropOpacity = Literal[
    'backdrop-opacity-0',
    'backdrop-opacity-5',
    'backdrop-opacity-10',
    'backdrop-opacity-20',
    'backdrop-opacity-25',
    'backdrop-opacity-30',
    'backdrop-opacity-40',
    'backdrop-opacity-50',
    'backdrop-opacity-60',
    'backdrop-opacity-70',
    'backdrop-opacity-75',
    'backdrop-opacity-80',
    'backdrop-opacity-90',
    'backdrop-opacity-95',
    'backdrop-opacity-100'
]

BackdropSaturate = Literal[
    'backdrop-saturate-0',
    'backdrop-saturate-50',
    'backdrop-saturate-100',
    'backdrop-saturate-150',
    'backdrop-saturate-200'
]

BackdropSepia = Literal[
    'backdrop-sepia-0',
    'backdrop-sepia'
]


class Filters:

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

    def blur(self, _blur: Blur):
        """Utilities for applying blur filters to an element."""
        self.__add(_blur)
        return self

    def brightness(self, _brightness: Brightness):
        """Utilities for applying brightness filters to an element."""
        self.__add(_brightness)
        return self

    def contrast(self, _contrast: Contrast):
        """Utilities for applying contrast filters to an element."""
        self.__add(_contrast)
        return self

    def drop_shadow(self, _drop_shadow: DropShadow):
        """Utilities for applying drop-shadow filters to an element."""
        self.__add(_drop_shadow)
        return self

    def grayscale(self, _grayscale: Grayscale):
        """Utilities for applying grayscale filters to an element."""
        self.__add(_grayscale)
        return self

    def hue_rotate(self, _hue_rotate: HueRotate):
        """Utilities for applying hue-rotate filters to an element."""
        self.__add(_hue_rotate)
        return self

    def invert(self, _invert: Invert):
        """Utilities for applying invert filters to an element."""
        self.__add(_invert)
        return self

    def saturate(self, _saturate: Saturate):
        """Utilities for applying saturation filters to an element."""
        self.__add(_saturate)
        return self

    def sepia(self, _sepia: Sepia):
        """Utilities for applying sepia filters to an element."""
        self.__add(_sepia)
        return self

    def backdrop_blur(self, _backdrop_blur: BackdropBlur):
        """Utilities for applying backdrop blur filters to an element."""
        self.__add(_backdrop_blur)
        return self

    def backdrop_brightness(self, _backdrop_brightness: BackdropBrightness):
        """Utilities for applying backdrop brightness filters to an element."""
        self.__add(_backdrop_brightness)
        return self

    def backdrop_contrast(self, _backdrop_contrast: BackdropContrast):
        """Utilities for applying backdrop contrast filters to an element."""
        self.__add(_backdrop_contrast)
        return self

    def backdrop_grayscale(self, _backdrop_grayscale: BackdropGrayscale):
        """Utilities for applying backdrop grayscale filters to an element."""
        self.__add(_backdrop_grayscale)
        return self

    def backdrop_hue_rotate(self, _backdrop_hue_rotate: BackdropHueRotate):
        """Utilities for applying backdrop hue-rotate filters to an element."""
        self.__add(_backdrop_hue_rotate)
        return self

    def backdrop_invert(self, _backdrop_invert: BackdropInvert):
        """Utilities for applying backdrop invert filters to an element."""
        self.__add(_backdrop_invert)
        return self

    def backdrop_opacity(self, _backdrop_opacity: BackdropOpacity):
        """Utilities for applying backdrop opacity filters to an element."""
        self.__add(_backdrop_opacity)
        return self

    def backdrop_saturate(self, _backdrop_saturate: BackdropSaturate):
        """Utilities for applying backdrop saturation filters to an element."""
        self.__add(_backdrop_saturate)
        return self

    def backdrop_sepia(self, _backdrop_sepia: BackdropSepia):
        """Utilities for applying backdrop sepia filters to an element."""
        self.__add(_backdrop_sepia)
        return self
