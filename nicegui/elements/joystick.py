import justpy as jp
import os.path
from .element import Element

class JoystickView(jp.JustpyBaseComponent):

    vue_type = 'joystick'

    def __init__(self, on_move):

        self.pages = {}
        self.classes = ''
        self.options = jp.Dict()

        self.on_move = on_move

        super().__init__()
        self.allowed_events = ['onMove']
        self.initialize(temp=False, onMove=self.handle_move)

    def add_page(self, wp: jp.WebPage):

        marker = '<!--' + self.__module__ + '-->\n'
        if marker not in wp.head_html:
            wp.head_html += marker
            wp.head_html += '<script src="https://cdn.jsdelivr.net/npm/nipplejs@0.9.0/dist/nipplejs.min.js"></script>\n'

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

    def handle_move(self, msg):

        self.on_move(msg.data)

class Joystick(Element):

    def __init__(self, *, on_move):

        super().__init__(JoystickView(on_move))
