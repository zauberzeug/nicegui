import asyncio

from typing_extensions import Self

from ..defaults import DEFAULT_PROP, resolve_defaults
from ..events import ClickEventArguments, Handler, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement


class Button(IconElement, TextElement, DisableableElement, BackgroundColorElement):

    @resolve_defaults
    def __init__(self,
                 text: str = '', *,
                 on_click: Handler[ClickEventArguments] | None = None,
                 color: str | None = DEFAULT_PROP | 'primary',
                 icon: str | None = DEFAULT_PROP | None,
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

    def _render_markdown(self) -> str:
        if label := self._props.get('label'):
            return f'[Button: {label}]'
        if aria_label := self._props.get('aria-label'):
            return f'[Button: {aria_label}]'
        if icon := self._props.get('icon'):
            return f'[Button: icon:{icon}]'
        children = self._children_to_markdown().strip()
        if children and '\n' not in children and '[' not in children and ']' not in children:
            # only surface single plain lines of child content that doesn't garble the "[Button: ...]" wrapper
            return f'[Button: {children}]'
        return '[Button]'

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text

    async def clicked(self) -> None:
        """Wait until the button is clicked."""
        event = asyncio.Event()
        self.on('click', event.set, [])
        await self.client.connected()
        await event.wait()
