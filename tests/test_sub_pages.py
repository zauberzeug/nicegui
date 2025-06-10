import pytest

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
        ui.link('goto other with slash', '/other/')

    def child2():
        ui.link('goto main', '/')
        ui.link('goto this path with slash', '/other/')

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

    screen.click('goto main')
    screen.click('goto other with slash')
    screen.should_contain('goto main')
    screen.click('goto this path with slash')
    screen.should_contain('goto main')


def test_passing_element_to_sub_page(screen: Screen):
    @ui.page('/')
    @ui.page('/other')
    def index():
        title = ui.label()
        ui.sub_pages({
            '/': lambda: child(title),
            '/other': lambda: child2(title)
        })

    def child(title: ui.label):
        title.set_text('child title')
        ui.link('goto other', '/other')

    def child2(title: ui.label):
        title.set_text('other title')
        ui.link('goto main', '/')

    screen.open('/')
    screen.should_contain('child title')
    screen.click('goto other')
    screen.should_contain('other title')
    screen.click('goto main')
    screen.should_contain('child title')


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
    screen.open('/one/')  # NOTE: having a slash at the end of the path should not cause an error
    screen.should_contain('one')
    screen.should_not_contain('two')


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


def test_parameterized_sub_pages(screen: Screen):
    main_content_calls = 0

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        ui.link('goto main', '/')
        ui.link('goto one', '/one-1')
        ui.link('goto two', '/two/two')
        ui.link('goto wrong match', '/two-3')
        ui.sub_pages({
            '/': main,
            '/one-{idx}': one,
            '/two/{idx}': two,
        })

    def main():
        nonlocal main_content_calls
        main_content_calls += 1
        ui.label('main_content')

    def one(idx: int):
        ui.label(f'one-{idx}-{isinstance(idx, int)}')

    def two(idx: str):
        ui.label(f'two-{idx}')

    screen.open('/')
    screen.should_contain('main_content')
    assert screen.current_path == '/'
    screen.click('goto one')
    screen.should_contain('one-1-True')
    assert screen.current_path == '/one-1'
    screen.click('goto two')
    screen.should_contain('two-two')
    assert screen.current_path == '/two/two'
    assert main_content_calls == 1
    screen.click('goto wrong match')
    screen.should_not_contain('main_content')
    screen.should_not_contain('one-1-True')
    screen.should_not_contain('two-two')
    screen.should_contain('404: sub page /two-3 not found')
    assert screen.current_path == '/two-3'
    assert main_content_calls == 1


def test_sub_page_with_default_parameter(screen: Screen):
    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        ui.sub_pages({
            '/': item_page,
            '/{item}': item_page,
        })

    def item_page(item: str = 'nothing'):
        ui.label(f'item: {item}')
    screen.open('/')
    screen.should_contain('item: nothing')
    assert screen.current_path == '/'
    screen.open('/3')
    screen.should_contain('item: 3')
    assert screen.current_path == '/3'


def test_sub_page_changing_via_navigate_to(screen: Screen):
    index_calls = 0

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        nonlocal index_calls
        index_calls += 1
        ui.button('go', on_click=lambda: ui.navigate.to('/test'))
        ui.sub_pages({
            '/': main_content,
            '/{item}': item_content,
        })

    def main_content():
        ui.label('main-content')

    def item_content(item: str):
        ui.label(f'item: {item}')

    screen.open('/')
    screen.should_contain('main-content')
    screen.click('go')
    screen.should_contain('item: test')
    assert index_calls == 1


def test_navigate_to_new_tab_fallback(screen: Screen):
    """Test that ui.navigate.to with new_tab=True always uses normal navigation."""
    index_calls = 0

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        nonlocal index_calls
        index_calls += 1
        ui.button('new tab', on_click=lambda: ui.navigate.to('/internal', new_tab=True))
        ui.sub_pages({
            '/': main_content,
            '/internal': internal_content,
        })

    def main_content():
        ui.label('main-content')

    def internal_content():
        ui.label('internal-content')

    screen.open('/')
    screen.should_contain('main-content')
    assert index_calls == 1

    # NOTE: even though this is a sub page route, new_tab=True should use normal navigation
    screen.click('new tab')
    screen.wait(0.5)
    screen.switch_to(1)
    screen.should_contain('internal-content')


def test_adding_sub_pages_after_initialization(screen: Screen):
    @ui.page('/')
    def index():
        pages = ui.sub_pages()
        pages.add('/', lambda: main_content(pages))

    def main_content(pages: ui.sub_pages):
        ui.button('add sub page', on_click=lambda: pages.add('/sub', sub_content))
        ui.button('goto sub', on_click=lambda: ui.navigate.to('/sub'))

    def sub_content():
        ui.label('sub-content')

    screen.open('/')
    screen.click('goto sub')
    assert screen.current_path == '/sub'
    screen.should_contain('404')
    screen.should_contain("This page doesn't exist")
    screen.open('/')
    screen.click('add sub page')
    screen.click('goto sub')
    screen.should_contain('sub-content')


@pytest.mark.parametrize('page_route', ['/foo/{_:path}', '/foo/sub', '/foo/sub/', '/{_:str}/sub'])
def test_starting_on_non_root_path(screen: Screen, page_route: str):
    @ui.page('/foo')
    @ui.page(page_route)
    def index():
        ui.sub_pages({'/': main_content, '/sub': sub_content}, root_path='/foo')

    def main_content():
        ui.label('main-content')
        ui.link('goto sub', '/foo/sub')

    def sub_content():
        ui.label('sub-content')
        ui.link('goto main', '/foo')

    screen.open('/foo/sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'
    screen.click('goto main')
    screen.should_contain('main-content')
    assert screen.current_path == '/foo'
    screen.click('goto sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'
    screen.click('goto main')
    screen.should_contain('main-content')
    screen.click('goto sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'


def test_links_pointing_to_path_which_is_not_a_sub_page(screen: Screen):
    @ui.page('/')
    def index():
        ui.link('goto main', '/')
        ui.link('goto sub', '/sub')
        ui.link('goto other', '/other')
        ui.sub_pages({'/': main, '/sub': sub})

    def main():
        ui.label('main')

    def sub():
        ui.label('sub')

    @ui.page('/other')
    def other():
        ui.label('other page')

    screen.open('/')
    screen.click('goto sub')
    screen.should_contain('sub')
    assert screen.current_path == '/sub'
    screen.click('goto other')
    screen.should_contain('other page')
    assert screen.current_path == '/other'


def test_navigate_to_path_which_is_not_a_sub_page(screen: Screen):
    @ui.page('/')
    def index():
        ui.button('goto main', on_click=lambda: ui.navigate.to('/'))
        ui.button('goto sub', on_click=lambda: ui.navigate.to('/sub'))
        ui.button('goto other', on_click=lambda: ui.navigate.to('/other'))
        ui.sub_pages({'/': main, '/sub': sub})

    def main():
        ui.label('main')

    def sub():
        ui.label('sub')

    @ui.page('/other')
    def other():
        ui.label('other page')

    screen.open('/')
    screen.click('goto sub')
    screen.should_contain('sub')
    assert screen.current_path == '/sub'
    screen.click('goto other')
    screen.should_contain('other page')
    assert screen.current_path == '/other'


def test_multiple_sub_pages_with_same_path(screen: Screen):
    @ui.page('/')
    def index():
        ui.sub_pages({'/': main, '/other': other})
        ui.sub_pages({'/': main2, '/other': other2})
        ui.link('goto other', '/other')

    def main():
        ui.label('main content')

    def main2():
        ui.label('main2 content')

    def other():
        ui.label('other content')

    def other2():
        ui.label('other2 content')

    screen.open('/')
    screen.should_contain('main content')
    screen.should_contain('main2 content')
    screen.should_not_contain('other content')
    screen.should_not_contain('other2 content')
    screen.click('goto other')
    screen.should_contain('other content')
    screen.should_contain('other2 content')
    screen.should_not_contain('main content')
    screen.should_not_contain('main2 content')
