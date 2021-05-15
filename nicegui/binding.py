from typing import Any
import asyncio

class Binding:

    all_bindings = []

    def __init__(self, element, element_attribute: str, model: Any, model_attribute: str) -> None:

        self.element = element
        self.element_attribute = element_attribute
        self.model = model
        self.model_attribute = model_attribute

    def get_model_value(self):

        if isinstance(self.model, dict):
            return self.model[self.model_attribute]
        else:
            return getattr(self.model, self.model_attribute)

    def set_model_value(self, value):

        if isinstance(self.model, dict):
            self.model[self.model_attribute] = value
        else:
            setattr(self.model, self.model_attribute, value)

    async def update_element(self):

        model_value = self.get_model_value()
        element_value = getattr(self.element, self.element_attribute)
        if element_value != model_value:
            setattr(self.element, self.element_attribute, model_value)
            await self.element.parent_view.update()

    def update_model(self):

        model_value = self.get_model_value()
        element_value = getattr(self.element, self.element_attribute)
        if model_value != element_value:
            self.set_model_value(element_value)

    @staticmethod
    async def loop():

        while True:

            for binding in Binding.all_bindings:
                await binding.update_element()

            await asyncio.sleep(0.1)
