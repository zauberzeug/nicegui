from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_page_title(screen: SeleniumScreen):
    ui.page_title('Initial title')
    ui.button('Change title', on_click=lambda: ui.page_title('"New title"'))

    @ui.page('/{title}')
    def page(title: str):
        ui.page_title(f'Title: {title}')

    screen.open('/')
    screen.wait(0.5)
    screen.should_contain('Initial title')

    screen.click('Change title')
    screen.wait(0.5)
    screen.should_contain('"New title"')

    screen.open('/test')
    screen.wait(0.5)
    screen.should_contain('Title: test')
