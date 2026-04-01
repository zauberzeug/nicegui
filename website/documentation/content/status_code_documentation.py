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


@doc.demo('Conditional 404', '''
    You can use `ui.status_code` to return a 404 status code when an item is not found.
    This is useful for SEO and for signaling to clients that a page does not exist.
''')
def item_demo() -> None:
    @ui.page('/item/{item_id}')
    def item_page(item_id: str):
        if 'a' <= item_id <= 'c':
            ui.label(f'This is item {item_id}')
        else:
            ui.status_code(404)
            ui.label('Page not found')

    # @ui.page('/')
    def page():
        ui.link('Show item A', '/item/a')
        ui.link('Show item B', '/item/b')
        ui.link('Show item X', '/item/x')
    page()  # HIDE
