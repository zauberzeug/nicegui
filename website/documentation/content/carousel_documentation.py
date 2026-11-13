from nicegui import ui

from . import doc


@doc.demo(ui.carousel)
def main_demo() -> None:
    with ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://nicegui.io/images/mug/270/180').classes('w-[270px]')
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://nicegui.io/images/feet/270/180').classes('w-[270px]')
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://nicegui.io/images/bench/270/180').classes('w-[270px]')


doc.reference(ui.carousel)
