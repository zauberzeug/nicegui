import asyncio
from typing import Any, Callable, Optional

from ..events import ClickEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement


class Button(TextElement, DisableableElement, BackgroundColorElement):
    """A button element that can be used in GUI applications.

    This element is based on Quasar's [QBtn](https://quasar.dev/vue-components/button) component.

    Args:
    
        - text (str, optional): The label of the button. Defaults to ''.
        - on_click (Optional[Callable[..., Any]], optional): Callback function to be invoked when the button is pressed. Defaults to None.
        - color (Optional[str], optional): The color of the button. It can be a Quasar color, a Tailwind color, or a CSS color. 
            If a Quasar color is used, the button will be styled according to the Quasar theme, including the color of the text.
            Note that there are colors like "red" that are both a Quasar color and a CSS color.
            In such cases, the Quasar color will be used. Defaults to 'primary'.
        - icon (Optional[str], optional): The name of an icon to be displayed on the button. Defaults to None.

    Attributes:
        - tag (str): The HTML tag used to render the button.
        - text (str): The label of the button.
        - background_color (str): The background color of the button.

    Example:
        >>> button = Button(text='Click me', on_click=handle_button_click, color='red', icon='fas fa-heart')
        >>> button.clicked()
        # Waits until the button is clicked
    """

    def __init__(self,
                     text: str = '', *,
                     on_click: Optional[Callable[..., Any]] = None,
                     color: Optional[str] = 'primary',
                     icon: Optional[str] = None,
                     ) -> None:
            """Button

            This element is based on Quasar's [QBtn ](https://quasar.dev/vue-components/button) component.
        
            Args:
            
                - text (str, optional): The label of the button. Defaults to ''.
                - on_click (Optional[Callable[..., Any]], optional): Callback function to be invoked when the button is pressed. Defaults to None.
                - color (Optional[str], optional): The color of the button. It can be a Quasar color, a Tailwind color, or a CSS color.
                    If a Quasar color is used, the button will be styled according to the Quasar theme, including the color of the text.
                    Note that there are colors like "red" that are both a Quasar color and a CSS color.
                    In such cases, the Quasar color will be used. Defaults to 'primary'.
                - icon (Optional[str], optional): The name of an icon to be displayed on the button. Defaults to None.

            Raises:
                None

            Returns:
                None

            """
            super().__init__(tag='q-btn', text=text, background_color=color)

            if icon:
                self._props['icon'] = icon

            if on_click:
                self.on('click', lambda _: handle_event(on_click, ClickEventArguments(sender=self, client=self.client)), [])

    def _text_to_model_text(self, text: str) -> None:
            """Converts the given text to the model text.

            This method is responsible for converting the provided text into the model text
            that will be displayed on the button. It updates the 'label' property of the button.

            Args:
                text (str): The text to be converted.

            Returns:
                None

            Example:
                button = Button()
                button._text_to_model_text("Click me")
            """
            self._props['label'] = text

    async def clicked(self) -> None:
            """
            Wait until the button is clicked.

            This method is used to wait for the button to be clicked. It creates an asyncio.Event object
            and sets up a callback function to trigger the event when the button is clicked. The method
            then waits for the client to be connected and for the event to be triggered.

            Returns:
                None

            Raises:
                None

            Example:
                button = Button()
                await button.clicked()
            """
            event = asyncio.Event()
            self.on('click', event.set, [])
            await self.client.connected()
            await event.wait()
