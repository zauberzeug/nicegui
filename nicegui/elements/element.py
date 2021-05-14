import justpy as jp
import asyncio
from ..utils import handle_exceptions, provide_arguments

class Element:

    wp: None
    view_stack = []
    bindings = []

    def __init__(self, view: jp.HTMLBaseComponent):

        self.parent_view = self.view_stack[-1]
        self.parent_view.add(view)
        view.add_page(self.wp)
        self.view = view

    def set_classes(self, classes: str):

        self.view.classes = classes
        return self

    def add_classes(self, classes: str):

        self.view.classes += ' ' + classes
        return self

    def set_style(self, style: str):

        self.view.style = style
        return self

    def add_style(self, style: str):

        self.view.style += ' ' + style
        return self

    def bind(self, view_attribute, model, model_attribute, interval, transform):

        async def loop():

            while True:
                model_value = transform(getattr(model, model_attribute))
                if getattr(self.view, view_attribute) != model_value:
                    print("Update view", view_attribute, 'to', model_value,
                          '/ was:', getattr(self.view, view_attribute))
                    setattr(self.view, view_attribute, model_value)
                    await self.parent_view.update()
                await asyncio.sleep(interval)

        self.bindings.append(loop())

    def bind_text(self, model, attribute, interval=0.1, transform=lambda x: x):

        self.bind('text', model, attribute, interval, transform)

    def bind_value(self, model, attribute, interval=0.1, transform=lambda x: x):

        self.bind('value', model, attribute, interval, transform)

        def update_model(_, event):
            model_value = transform(getattr(model, attribute))
            if model_value != transform(float(event.value)):
                print("Update model", attribute, 'to', event.value, '/ was:', model_value)
                setattr(model, attribute, event.value)

        self.view.on('change', handle_exceptions(update_model))
