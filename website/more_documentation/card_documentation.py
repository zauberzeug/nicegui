from nicegui import ui


def main_demo() -> None:
    with ui.card().tight() as card:
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')
