from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=missing-function-docstring


def test_switching_between_sub_pages(screen: Screen):
    index_calls = 0

    @ui.page('/')
    @ui.page('/other')
    def index():
        nonlocal index_calls
        index_calls += 1
        ui.label('some text before main content')
        ui.sub_pages({'/': child, '/other': child2})

    def child():
        ui.link('goto other', '/other')

    def child2():
        ui.link('goto main', '/')

    screen.open('/')
    assert index_calls == 1
    screen.should_contain('some text before main content')
    screen.should_contain('goto other')
    screen.should_not_contain('goto main')
    screen.click('goto other')
    assert index_calls == 1
    screen.should_contain('some text before main content')
    screen.should_contain('goto main')
    screen.should_not_contain('goto other')
    screen.selenium.back()
    assert index_calls == 1
    screen.should_contain('some text before main content')
    screen.should_contain('goto other')
    screen.should_not_contain('goto main')
    screen.selenium.forward()
    assert index_calls == 1
    screen.should_contain('some text before main content')
    screen.should_contain('goto main')
    screen.should_not_contain('goto other')


def test_accessing_sub_page_directly(screen: Screen):
    @ui.page('/two')
    @ui.page('/one')
    def index():
        ui.sub_pages({'/one': sub_page1, '/two': sub_page2})

    def sub_page1():
        ui.label('one')

    def sub_page2():
        ui.label('two')

    screen.open('/one')
    screen.should_contain('one')
    screen.should_not_contain('two')
    screen.open('/two')
    screen.should_contain('two')
    screen.should_not_contain('one')
