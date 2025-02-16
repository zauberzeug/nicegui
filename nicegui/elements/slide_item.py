from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import Self

from ..events import ClickEventArguments, GenericEventArguments, Handler, handle_event
from .mixins.disableable_element import DisableableElement

SlideSides = Literal['left', 'right', 'top', 'bottom']


class SlideSide(DisableableElement):
    def __init__(self,
                 side: SlideSides, *,
                 on_slide: Optional[Handler[GenericEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Side

        This element is based on Quasar's on the side slots of `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Side element can only be used as a child of the `SlideItem` element.

        :param side: side of the Slide Item where the slide should be added (`left`, `right`, `top`, `bottom`)
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__()

        self.side = side

        self._slide_item_parent = self._get_slide_parent()

        self._slide_item_parent.add_slot(side)
        self._slide_item_parent._props[f'{side}-color'] = color

        self.default_slot = self._slide_item_parent.slots[side]

        if side not in self._slide_item_parent._active_slides:
            self._slide_item_parent._active_slides.append(side)

        if on_slide:
            self.on_slide(on_slide)

    def _get_slide_parent(self) -> SlideItem:
        """Get parent slot and confirms it is of `SlideItem` type"""

        if self.parent_slot is None:
            raise ValueError('Parent slot can not be established')

        slide_item_parent = self.parent_slot.parent

        if not isinstance(slide_item_parent, SlideItem):
            raise ValueError('Incorrect parent used, `SlideSide` must inherit from `SlideItem`')

        return slide_item_parent

    def on_slide(self, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when the Slide Side is activated."""
        self._slide_item_parent.on(self.side, lambda _: handle_event(
            callback, GenericEventArguments(sender=self, client=self.client, args=self.side)))
        return self


class SlideItem(DisableableElement):
    def __init__(self,
                 on_change: Optional[Handler[ClickEventArguments]] = None):
        """Slide Item

        This element is based on Quasar's `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Slide Item element is related to the `Item` element and supports `ItemSection` for text, icons, etc.
        To add slide actions use in conjunction with `LeftSlide`, `RightSlide`, `TopSlide`, and `BottomSlide`

        :param on_change: callback which is invoked when any slide action is activated
        """
        super().__init__(tag='q-slide-item')

        self._active_slides: list[str] = []

        if on_change:
            self.on_change(on_change)

    def on_change(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the Slide Item is clicked."""
        self.on('action', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)))
        return self

    def reset(self) -> None:
        """Reset the Slide Item to initial state"""
        self.run_method('reset')

    @property
    def active_slides(self) -> list:
        """Returns a list of active Slide Sides"""
        return self._active_slides


class LeftSlide(SlideSide):
    def __init__(self,
                 on_slide: Optional[Handler[GenericEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Left Slide

        This element is based on Quasar's on the `Left` slot of `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Left Slide element can only be used as a child of the `SlideItem` element.

        :param on_slide: callback which is invoked when the left slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__('left', color=color, on_slide=on_slide)


class RightSlide(SlideSide):
    def __init__(self,
                 on_slide: Optional[Handler[GenericEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Right Slide

        This element is based on Quasar's on the `Right` slot of `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Right Slide element can only be used as a child of the `SlideItem` element.

        :param on_slide: callback which is invoked when the right slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__('right', color=color, on_slide=on_slide)


class TopSlide(SlideSide):
    def __init__(self,
                 on_slide: Optional[Handler[GenericEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Top Slide

        This element is based on Quasar's on the `Top` slot of `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Top Slide element can only be used as a child of the `SlideItem` element.

        :param on_slide: callback which is invoked when the top slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__('top', color=color, on_slide=on_slide)


class BottomSlide(SlideSide):
    def __init__(self,
                 on_slide: Optional[Handler[GenericEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """Bottom Slide

        This element is based on Quasar's on the `Bottom` slot of `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        The Bottom Slide element can only be used as a child of the `SlideItem` element.

        :param on_slide: callback which is invoked when the bottom slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """
        super().__init__('bottom', color=color, on_slide=on_slide)
