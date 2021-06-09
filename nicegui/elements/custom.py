import justpy as jp
import os.path
from .element import Element

class CustomView(jp.JustpyBaseComponent):

    vue_type = 'custom'

    def __init__(self, on_change):

        self.pages = {}
        self.classes = ''
        self.options = jp.Dict(value=0)

        self.on_change = on_change

        super().__init__()
        self.allowed_events = ['onAdd']
        self.initialize(temp=False, onAdd=self.onAdd)

    def add_page(self, wp: jp.WebPage):

        jp.component_file_list += ['file?path=' + os.path.realpath(__file__).replace('.py', '.js')]

        super().add_page(wp)

    def react(self, _):

        pass

    def convert_object_to_dict(self):

        return {
            'vue_type': self.vue_type,
            'id': self.id,
            'show': True,
            'options': self.options,
        }

    def onAdd(self, msg):

        self.options.value += msg.number
        self.on_change(self.options.value)

class Custom(Element):

    def __init__(self, *, on_change):

        super().__init__(CustomView(on_change))

    def add(self, number: str):

        self.view.options.value += number
        self.view.on_change(self.view.options.value)
