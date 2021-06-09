import justpy as jp
import os.path
from .element import Element

class ThreeView(jp.JustpyBaseComponent):

    vue_type = 'three'

    def __init__(self, on_click):

        self.pages = {}
        self.classes = ''
        self.options = jp.Dict(camera_z=4)

        self.on_click = on_click

        super().__init__()
        self.allowed_events = ['onClick']
        self.initialize(temp=False, onClick=self.handle_click)

    def add_page(self, wp: jp.WebPage):

        marker = '<!--' + self.__module__ + '-->\n'
        if marker not in wp.head_html:
            wp.head_html += marker
            wp.head_html += '<script src="https://cdn.jsdelivr.net/npm/three@0.129.0/build/three.min.js"></script>\n'
            wp.head_html += '<script src="https://cdn.jsdelivr.net/npm/three@0.129.0/examples/js/controls/OrbitControls.js"></script>\n'

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

    def handle_click(self, msg):

        self.on_click(msg.objects)

class Three(Element):

    def __init__(self, *, on_click):

        super().__init__(ThreeView(on_click))

    def move_camera(self, z):

        self.view.options.camera_z = z
