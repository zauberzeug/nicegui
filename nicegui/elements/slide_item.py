from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import Self

from ..events import ClickEventArguments, GenericEventArguments, Handler, handle_event
from .mixins.disableable_element import DisableableElement

SlideSides = Literal['left', 'right', 'top', 'bottom']


class SlideItem(DisableableElement):
    def __init__(self,
                 on_change: Optional[Handler[ClickEventArguments]] = None):
        """Slide Item

        This element is based on Quasar's `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        To add slide actions to a specific side (`left`, `right`, `top`, `bottom`) use the `slide` method.

        :param on_change: callback which is invoked when any slide action is activated
        """

        super().__init__(tag='q-slide-item')

        self._active_slides: list[str] = []

        if on_change:
            self.on_change(on_change)

    def slide(self,
              side: SlideSides, *,
              on_slide: Optional[Handler[GenericEventArguments]] = None,
              color: Optional[str] = 'primary',
              ) -> Self:
        """Slide

        This method adds a slide action to a specified side of the `SlideItem`

        :param side: side of the Slide Item where the slide should be added (`left`, `right`, `top`, `bottom`)
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        """

        if color:
            self._props[f'{side}-color'] = color

        if on_slide:
            self.on_slide(side, on_slide)

        if side not in self._active_slides:
            self._active_slides.append(side)

        return self.add_slot(side)

    def on_change(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the Slide Item is changed."""
        self.on('action', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)))
        return self

    def on_slide(self, side: SlideSides, callback: Handler[GenericEventArguments]) -> Self:
        """Add a callback to be invoked when a Slide Side is activated."""
        self.on(side, lambda _: handle_event(callback, GenericEventArguments(sender=self, client=self.client, args=side)))
        return self

    def reset(self) -> None:
        """Reset the Slide Item to initial state"""
        self.run_method('reset')

    @property
    def active_slides(self) -> list:
        """Returns a list of active Slide Sides"""
        return self._active_slides
