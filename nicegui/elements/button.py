import asyncio
from typing import Awaitable, Callable, Union

import justpy as jp

from .element import Element
from ..utils import handle_exceptions, provide_arguments, EventArguments

class Button(Element):

    def __init__(self,
                 text: str = '',
                 *,
                 on_click: Union[Callable, Awaitable] = None,
                 ):
        """Button Element

        :param text: the label of the button
        :param on_click: callback which is invoked when button is pressed
        """

        view = jp.QButton(label=text, color='primary')

        if on_click is not None:
            if asyncio.iscoroutinefunction(on_click):

                def async_provide_arguments(func, *keys):
                    def inner_function(sender, event):
                        async def execute_function():
                            try:
                                await func()
                            except TypeError:
                                await func(EventArguments(sender, **{key: event[key] for key in keys}))

                            await self.parent_view.update()

                        asyncio.get_event_loop().create_task(execute_function())
                    return inner_function

                view.on('click', handle_exceptions(async_provide_arguments(on_click)))
            else:
                view.on('click', handle_exceptions(provide_arguments(on_click)))

        super().__init__(view)

    @property
    def text(self):
        return self.view.label

    @text.setter
    def text(self, text: any):
        self.view.label = text

    def set_text(self, text: str):
        self.text = text

    def bind_text_to(self, target, forward=lambda x: x):
        self.text.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_text_from(self, target, backward=lambda x: x):
        self.text.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_text(self, target, forward=lambda x: x, backward=lambda x: x):
        self.text.bind(target, forward=forward, backward=backward, nesting=1)
        return self
