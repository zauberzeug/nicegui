from typing import Literal, Optional

from ..element import Element


class Skeleton(Element):

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
                 ] = 'rect',
                 *,
                 tag: str = 'div',
                 animation: Literal[
                     'wave',
                     'pulse',
                     'pulse-x',
                     'pulse-y',
                     'fade',
                     'blink',
                     'none',
                 ] = 'wave',
                 animation_speed: float = 1.5,
                 square: bool = False,
                 bordered: bool = False,
                 size: Optional[str] = None,
                 width: Optional[str] = None,
                 height: Optional[str] = None,
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
        if type != 'rect':
            self._props['type'] = type
        if tag != 'div':
            self._props['tag'] = tag
        if animation != 'wave':
            self._props['animation'] = animation
        if animation_speed != 1.5:
            self._props['animation-speed'] = animation_speed
        if square:
            self._props['square'] = True
        if bordered:
            self._props['bordered'] = True
        if size:
            self._props['size'] = size
        if width:
            self._props['width'] = width
        if height:
            self._props['height'] = height
