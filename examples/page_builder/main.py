from nicegui import ui
from nicegui.page import page
from nicegui.page_builder import PageBuilder, PageRouter


class DemoPage(PageBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        ui.link('Go to /about', '/about')


@page('/')
def index():
    router = PageRouter()
    router.add('/', DemoPage, default=True)


ui.run(show=False)
