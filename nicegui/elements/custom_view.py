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
        for dependency in self.vue_dependencies:
            is_remote = dependency.startswith('http://') or dependency.startswith('https://')
            src = dependency if is_remote else f'lib/{dependency}'
            if src not in jp.component_file_list:
                jp.component_file_list += [src]
                if not is_remote:
                    filepath = f'{os.path.dirname(self.vue_filepath)}/{src}'
                    route = Route(f'/{src}', lambda _, filepath=filepath: FileResponse(filepath))
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
