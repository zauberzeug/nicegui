from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import Self

from ..events import Handler, SlideEventArguments, handle_event
from ..slot import Slot
from .item import Item
from .label import Label
from .mixins.disableable_element import DisableableElement

SlideSide = Literal['left', 'right', 'top', 'bottom']


class SlideItem(DisableableElement):

    def __init__(self, text: str = '', *, on_slide: Optional[Handler[SlideEventArguments]] = None) -> None:
        """Slide Item

        This element is based on Quasar's `QSlideItem <https://quasar.dev/vue-components/slide-item/>`_ component.

        If the ``text`` parameter is provided, a nested ``ui.item`` element will be created with the given text.
        If you want to customize how the text is displayed, you can place custom elements inside the slide item.

        To fill slots for individual slide actions, use the ``left``, ``right``, ``top``, or ``bottom`` methods or
        the ``action`` method with a side argument ("left", "right", "top", or "bottom").

        Once a slide action has occurred, the slide item can be reset back to its initial state using the ``reset`` method.

        *Added in version 2.12.0*

        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when any slide action is activated
        """
        super().__init__(tag='q-slide-item')

        if text:
            with self:
                Item(text)

        if on_slide:
            self.on_slide(None, on_slide)

    def action(self,
               side: SlideSide,
               text: str = '', *,
               on_slide: Optional[Handler[SlideEventArguments]] = None,
               color: Optional[str] = 'primary',
               ) -> Slot:
        """Add a slide action to a specified side.

        :param side: side of the slide item where the slide should be added ("left", "right", "top", "bottom")
        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or ``None``, default: "primary")
        """
        if color:
            self._props[f'{side}-color'] = color

        if on_slide:
            self.on_slide(side, on_slide)

        slot = self.add_slot(side)
        if text:
            with slot:
                Label(text)

        return slot

    def left(self,
             text: str = '', *,
             on_slide: Optional[Handler[SlideEventArguments]] = None,
             color: Optional[str] = 'primary',
             ) -> Slot:
        """Add a slide action to the left side.

        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or ``None``, default: "primary")
        """
        return self.action('left', text=text, on_slide=on_slide, color=color)

    def right(self,
              text: str = '', *,
              on_slide: Optional[Handler[SlideEventArguments]] = None,
              color: Optional[str] = 'primary',
              ) -> Slot:
        """Add a slide action to the right side.

        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or ``None``, default: "primary")
        """
        return self.action('right', text=text, on_slide=on_slide, color=color)

    def top(self,
            text: str = '', *,
            on_slide: Optional[Handler[SlideEventArguments]] = None,
            color: Optional[str] = 'primary',
            ) -> Slot:
        """Add a slide action to the top side.

        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or ``None``, default: "primary")
        """
        return self.action('top', text=text, on_slide=on_slide, color=color)

    def bottom(self,
               text: str = '', *,
               on_slide: Optional[Handler[SlideEventArguments]] = None,
               color: Optional[str] = 'primary',
               ) -> Slot:
        """Add a slide action to the bottom side.

        :param text: text to be displayed (default: "")
        :param on_slide: callback which is invoked when the slide action is activated
        :param color: the color of the slide background (either a Quasar, Tailwind, or CSS color or ``None``, default: "primary")
        """
        return self.action('bottom', text=text, on_slide=on_slide, color=color)

    def on_slide(self, side: SlideSide | None, handler: Handler[SlideEventArguments]) -> Self:
        """Add a callback to be invoked when the slide action is activated."""
        self.on(side or 'action', lambda e: handle_event(handler, SlideEventArguments(sender=self,
                                                                                      client=self.client,
                                                                                      side=e.args.get('side', side))))
        return self

    def reset(self) -> None:
        """Reset the slide item to its initial state."""
        self.run_method('reset')
