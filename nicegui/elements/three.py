import os.path
from .custom_view import CustomView
from .element import Element

class ThreeView(CustomView):

    vue_type = 'three'
    vue_filepath = os.path.realpath(__file__).replace('.py', '.js')
    vue_dependencies = [
        'https://cdn.jsdelivr.net/npm/three@0.129.0/build/three.min.js',
        'https://cdn.jsdelivr.net/npm/three@0.129.0/examples/js/controls/OrbitControls.js',
    ]

    def __init__(self, on_click):

        self.on_click = on_click

        super().__init__(camera_z=4)
        self.allowed_events = ['onClick']
        self.initialize(temp=False, onClick=self.handle_click)

    def handle_click(self, msg):

        self.on_click(msg.objects)

class Three(Element):

    def __init__(self, *, on_click):

        super().__init__(ThreeView(on_click))

    def move_camera(self, z):

        self.view.options.camera_z = z
