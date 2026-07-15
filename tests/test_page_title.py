import asyncio

from nicegui import ui
from nicegui.testing import Screen


def test_page_title(screen: Screen):
    @ui.page('/')
    def page():
        ui.page_title('Initial title')
        ui.button('Change title', on_click=lambda: ui.page_title('"New title"'))

    @ui.page('/{title}')
    def page_with_title(title: str):
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


def test_page_title_after_await_in_async_sub_page(screen: Screen):
    async def sub():
        ui.page_title('before')
        await asyncio.sleep(0)  # resumes after the response is built, before the socket connects
        ui.page_title('after')

    @ui.page('/')
    def index():
        ui.sub_pages({'/': sub})

    screen.open('/')
    screen.wait_for(lambda: screen.selenium.title == 'after')
