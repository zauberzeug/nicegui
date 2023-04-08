from nicegui import ui


def main_demo() -> None:
    @ui.page('/other_page')
    def other_page():
        ui.label('Welcome to the other side')
        ui.link('Back to main page', '/documentation#page')

    @ui.page('/dark_page', dark=True)
    def dark_page():
        ui.label('Welcome to the dark side')
        ui.link('Back to main page', '/documentation#page')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)
