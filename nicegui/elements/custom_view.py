import justpy as jp
import os.path
from starlette.routing import Route
from starlette.responses import FileResponse

class CustomView(jp.JustpyBaseComponent):

    vue_dependencies = []

    def __init__(self, vue_type, filepath, dependencies=[], **options):

        self.vue_type = vue_type
        self.vue_filepath = os.path.realpath(filepath).replace('.py', '.js')
        self.vue_dependencies = dependencies

        self.pages = {}
        self.classes = ''
        self.style = ''
        self.options = jp.Dict(**options)

        super().__init__(temp=False)

    def add_page(self, wp: jp.WebPage):

        marker = '<!--' + self.__module__ + '-->\n'
        if marker not in wp.head_html:
            wp.head_html += marker
            for dependency in self.vue_dependencies:
                if dependency.startswith('http://') or dependency.startswith('https://'):
                    wp.head_html += f'<script src="{dependency}"></script>\n'
                else:
                    wp.head_html += f'<script src="lib/{dependency}"></script>\n'
                    filepath = f'{os.path.dirname(self.vue_filepath)}/lib/{dependency}'
                    route = Route(f'/lib/{dependency}', lambda _, filepath=filepath: FileResponse(filepath))
                    jp.app.routes.insert(0, route)

        if self.vue_filepath not in jp.component_file_list:
            filename = os.path.basename(self.vue_filepath)
            jp.app.routes.insert(0, Route(f'/{filename}', lambda _: FileResponse(self.vue_filepath)))
            jp.component_file_list += [filename]

        super().add_page(wp)

    def react(self, _):

        pass

    def convert_object_to_dict(self):

        return {
            'vue_type': self.vue_type,
            'id': self.id,
            'show': True,
            'classes': self.classes,
            'style': self.style,
            'options': self.options,
        }
