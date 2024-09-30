import asyncio
from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement


class Button(IconElement, TextElement, DisableableElement, BackgroundColorElement):

    def __init__(self,
                 text: str = '', *,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 icon: Optional[str] = None,
                 ) -> None:
        """Button

        This element is based on Quasar's `QBtn <https://quasar.dev/vue-components/button>`_ component.

        The ``color`` parameter accepts a Quasar color, a Tailwind color, or a CSS color.
        If a Quasar color is used, the button will be styled according to the Quasar theme including the color of the text.
        Note that there are colors like "red" being both a Quasar color and a CSS color.
        In such cases the Quasar color will be used.

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        :param color: the color of the button (either a Quasar, Tailwind, or CSS color or `None`, default: 'primary')
        :param icon: the name of an icon to be displayed on the button (default: `None`)
        """
        super().__init__(tag='q-btn', text=text, background_color=color, icon=icon)

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """Add a callback to be invoked when the button is clicked."""
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text

    async def clicked(self) -> None:
        """Wait until the button is clicked."""
        event = asyncio.Event()
        self.on('click', event.set, [])
        await self.client.connected()
        await event.wait()
