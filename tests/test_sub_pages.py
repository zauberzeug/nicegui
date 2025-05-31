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
    @ui.page('/')
    @ui.page('/{_:path}')
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


def test_sub_page_in_sub_page(screen: Screen):
    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        ui.link('goto main', '/')
        ui.link('goto sub', '/sub')
        ui.sub_pages({'/': main, '/sub': sub})

    def main():
        ui.label('main')

    def sub():
        ui.label('sub')
        ui.link('goto a', '/sub/a')
        ui.link('goto b', '/sub/b')
        ui.sub_pages({
            '/': sub_main,
            '/a': sub_page_a,
            '/b': sub_page_b
        })

    def sub_main():
        ui.label('sub-main')

    def sub_page_a():
        ui.label('sub-a')

    def sub_page_b():
        ui.label('sub-b')

    screen.open('/')
    screen.should_contain('main')
    screen.click('goto sub')
    screen.should_contain('sub-main')
    screen.click('goto a')
    screen.should_contain('sub-a')
    screen.click('goto b')
    screen.should_contain('sub-b')
    screen.click('goto main')
    screen.should_contain('main')
    screen.should_not_contain('sub-main')
    screen.should_not_contain('sub-a')
    screen.should_not_contain('sub-b')

    screen.open('/sub/a')
    screen.should_contain('sub-a')
