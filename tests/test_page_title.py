from nicegui import ui
from nicegui.testing import SharedScreen


def test_page_title(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.page_title('Initial title')
        ui.button('Change title', on_click=lambda: ui.page_title('"New title"'))

    @ui.page('/{title}')
    def page_with_title(title: str):
        ui.page_title(f'Title: {title}')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Initial title')

    shared_screen.click('Change title')
    shared_screen.wait(0.5)
    shared_screen.should_contain('"New title"')

    shared_screen.open('/test')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Title: test')
