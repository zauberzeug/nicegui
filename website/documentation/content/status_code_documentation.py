from nicegui import ui

from . import doc


@doc.demo(ui.status_code)
def main_demo() -> None:
    @ui.page('/teapot')
    def teapot_page():
        ui.status_code(418)
        ui.label("I'm a teapot")

    # @ui.page('/')
    def page():
        ui.link('Visit the teapot page', '/teapot')
    page()  # HIDE
