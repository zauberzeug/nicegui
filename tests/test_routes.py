from nicegui import ui
from starlette import responses

from .screen import Screen


def test_get(screen: Screen):
    @ui.get('/some/route')
    def some_route():
        return responses.PlainTextResponse('Ok')

    screen.open('/some/route')
    screen.should_contain('Ok')


def test_get_with_args(screen: Screen):
    @ui.get('/route/{id}')
    def route(id: int):
        return responses.PlainTextResponse(f'id={id}')

    screen.open('/route/42')
    screen.should_contain('id=42')


def test_page_with_args(screen: Screen):
    @ui.page('/page/{id}')
    def page(id: int):
        ui.label(f'Page {id}')

    screen.open('/page/42')
    screen.should_contain('Page 42')
