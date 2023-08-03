from nicegui import ui


def main_demo() -> None:
    with ui.carousel(animated=True, arrows=True, navigation=True).props('height=180px'):
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://picsum.photos/id/30/270/180').classes('w-[270px]')
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://picsum.photos/id/31/270/180').classes('w-[270px]')
        with ui.carousel_slide().classes('p-0'):
            ui.image('https://picsum.photos/id/32/270/180').classes('w-[270px]')
