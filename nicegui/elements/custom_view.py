import justpy as jp
import os.path
from typing import List
from starlette.routing import Route
from starlette.responses import FileResponse

class CustomView(jp.JustpyBaseComponent):

    def __init__(self, vue_type, **options):
        self.vue_type = vue_type

        self.pages = {}
        self.classes = ''
        self.style = ''
        self.options = jp.Dict(**options)
        self.components = []

        super().__init__(temp=False)

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

    @staticmethod
    def use(py_filepath: str, dependencies: List[str] = []):
        vue_filepath = os.path.realpath(py_filepath).replace('.py', '.js')

        for dependency in dependencies:
            is_remote = dependency.startswith('http://') or dependency.startswith('https://')
            src = dependency if is_remote else f'lib/{dependency}'
            if src not in jp.component_file_list:
                jp.component_file_list += [src]
                if not is_remote:
                    filepath = f'{os.path.dirname(vue_filepath)}/{src}'
                    route = Route(f'/{src}', lambda _, filepath=filepath: FileResponse(filepath))
                    jp.app.routes.insert(0, route)

        if vue_filepath not in jp.component_file_list:
            filename = os.path.basename(vue_filepath)
            jp.app.routes.insert(0, Route(f'/{filename}', lambda _: FileResponse(vue_filepath)))
            jp.component_file_list += [filename]
