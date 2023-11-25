from nicegui import app, ui

from ...model import UiElementDocumentation


class AddStaticFilesDocumentation(UiElementDocumentation, element=app.add_static_files):

    def main_demo(self) -> None:
        from nicegui import app

        app.add_static_files('/examples', 'examples')
        ui.label('Some NiceGUI Examples').classes('text-h5')
        ui.link('AI interface', '/examples/ai_interface/main.py')
        ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
        ui.link('Authentication', '/examples/authentication/main.py')
