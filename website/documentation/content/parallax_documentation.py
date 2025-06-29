from nicegui import ui

from . import doc


@doc.auto_execute
@doc.demo(ui.parallax)
def main_demo() -> None:
    @ui.page('/parallax_demo')
    def parallax_demo():
        ui.label('Dummy text...').classes('border h-screen w-full')

        with ui.parallax('https://cdn.quasar.dev/img/parallax2.jpg', height=300, speed=0.5) as parallax:
            ui.label('Text').classes('text-white')

        ui.label('Dummy text...').classes('border h-screen w-full')

    # END OF DEMO

    ui.link('Go to parallax demo', '/parallax_demo')


doc.reference(ui.parallax)
