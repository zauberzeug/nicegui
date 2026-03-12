from typing import Literal

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..element import Element


class Skeleton(Element):

    @resolve_defaults
    def __init__(self,
                 type: Literal[  # pylint: disable=redefined-builtin
                     'text',
                     'rect',
                     'circle',
                     'QBtn',
                     'QBadge',
                     'QChip',
                     'QToolbar',
                     'QCheckbox',
                     'QRadio',
                     'QToggle',
                     'QSlider',
                     'QRange',
                     'QInput',
                     'QAvatar',
                 ] = DEFAULT_PROP | 'rect',
                 *,
                 tag: str = DEFAULT_PROP | 'div',
                 animation: Literal[
                     'wave',
                     'pulse',
                     'pulse-x',
                     'pulse-y',
                     'fade',
                     'blink',
                     'none',
                 ] = DEFAULT_PROP | 'wave',
                 animation_speed: float = 1.5,
                 square: bool = DEFAULT_PROP | False,
                 bordered: bool = DEFAULT_PROP | False,
                 size: str | None = DEFAULT_PROP | None,
                 width: str | None = DEFAULT_PROP | None,
                 height: str | None = DEFAULT_PROP | None,
                 ) -> None:
        """Skeleton

        This element is based on Quasar's `QSkeleton <https://quasar.dev/vue-components/skeleton>`_ component.
        It serves as a placeholder for loading content in cards, menus and other component containers.
        See the `Quasar documentation <https://quasar.dev/vue-components/skeleton/#predefined-types>`_ for a list of available types.

        :param type: type of skeleton to display (default: "rect")
        :param tag: HTML tag to use for this element (default: "div")
        :param animation: animation effect of the skeleton placeholder (default: "wave")
        :param animation_speed: animation speed in seconds (default: 1.5)
        :param square: whether to remover border-radius so borders are squared (default: ``False``)
        :param bordered: whether to apply a default border to the component (default: ``False``)
        :param size: size in CSS units (overrides ``width`` and ``height``)
        :param width: width in CSS units (overridden by ``size`` if set)
        :param height: height in CSS units (overridden by ``size`` if set)
        """
        super().__init__('q-skeleton')
        self._props.set_optional('type', type if type != 'rect' else None)
        self._props.set_optional('tag', tag if tag != 'div' else None)
        self._props.set_optional('animation', animation if animation != 'wave' else None)
        self._props.set_optional('animation-speed', animation_speed if animation_speed != 1.5 else None)
        self._props.set_bool('square', square)
        self._props.set_bool('bordered', bordered)
        self._props.set_optional('size', size)
        self._props.set_optional('width', width)
        self._props.set_optional('height', height)
