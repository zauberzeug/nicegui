import pytest

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=missing-function-docstring


def test_switching_between_sub_pages(screen: Screen):
    calls = {'index': 0, 'a': 0, 'b': 0}

    @ui.page('/')
    @ui.page('/b')
    def index():
        calls['index'] += 1
        ui.label('Index')
        ui.sub_pages({'/': sub_page_a, '/b': sub_page_b})

    def sub_page_a():
        calls['a'] += 1
        ui.label('Page A')
        ui.link('Go to B', '/b')
        ui.link('Go to B with slash', '/b/')

    def sub_page_b():
        calls['b'] += 1
        ui.label('Page B')
        ui.link('Go to A', '/')
        ui.link('Go to B with slash', '/b/')

    screen.open('/')
    screen.should_contain('Index')
    screen.should_contain('Page A')
    screen.should_not_contain('Page B')
    assert calls == {'index': 1, 'a': 1, 'b': 0}

    screen.click('Go to B')
    screen.should_contain('Index')
    screen.should_contain('Page B')
    screen.should_not_contain('Page A')
    assert calls == {'index': 1, 'a': 1, 'b': 1}

    screen.selenium.back()
    screen.should_contain('Index')
    screen.should_contain('Page A')
    screen.should_not_contain('Page B')
    assert calls == {'index': 1, 'a': 2, 'b': 1}

    screen.selenium.forward()
    screen.should_contain('Index')
    screen.should_contain('Page B')
    screen.should_not_contain('Page A')
    assert calls == {'index': 1, 'a': 2, 'b': 2}

    screen.click('Go to A')
    screen.click('Go to B with slash')
    screen.should_contain('Page B')
    assert calls == {'index': 1, 'a': 3, 'b': 3}

    screen.click('Go to B with slash')
    screen.should_contain('Page B')
    assert calls == {'index': 1, 'a': 3, 'b': 4}


def test_passing_element_to_sub_page(screen: Screen):
    @ui.page('/')
    @ui.page('/other')
    def index():
        title = ui.label()
        ui.sub_pages({
            '/': lambda: main(title),
            '/other': lambda: other(title)
        })

    def main(title: ui.label):
        title.text = 'main title'
        ui.link('Go to other', '/other')

    def other(title: ui.label):
        title.text = 'other title'
        ui.link('Go to main', '/')

    screen.open('/')
    screen.should_contain('main title')

    screen.click('Go to other')
    screen.should_contain('other title')

    screen.click('Go to main')
    screen.should_contain('main title')


def test_opening_sub_pages_directly(screen: Screen):
    @ui.page('/')
    @ui.page('/{_:path}')
    def index():
        ui.sub_pages({
            '/one': one,
            '/two': two,
        })

    def one():
        ui.label('one')

    def two():
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
        ui.link('Go to main', '/')
        ui.link('Go to sub', '/sub')
        ui.sub_pages({
            '/': main,
            '/sub': sub,
        })

    def main():
        ui.label('main page')

    def sub():
        ui.label('sub page')
        ui.link('Go to A', '/sub/a')
        ui.link('Go to B', '/sub/b')
        ui.sub_pages({
            '/': sub_main,
            '/a': sub_page_a,
            '/b': sub_page_b
        })

    def sub_main():
        ui.label('sub main page')

    def sub_page_a():
        ui.label('sub A page')

    def sub_page_b():
        ui.label('sub B page')

    screen.open('/')
    screen.should_contain('main page')

    screen.click('Go to sub')
    screen.should_contain('sub main page')

    screen.click('Go to A')
    screen.should_contain('sub A page')

    screen.click('Go to B')
    screen.should_contain('sub B page')

    screen.click('Go to main')
    screen.should_contain('main page')
    screen.should_not_contain('sub main page')
    screen.should_not_contain('sub A page')
    screen.should_not_contain('sub B page')

    screen.open('/sub/a')
    screen.should_contain('sub A page')


def test_parameterized_sub_pages(screen: Screen):
    calls = {'main': 0}

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        ui.link('Go to main', '/')
        ui.link('Go to one', '/one-1')
        ui.link('Go to two', '/two/two')
        ui.link('Go to wrong match', '/two-3')
        ui.sub_pages({
            '/': main,
            '/one-{idx}': one,
            '/two/{idx}': two,
        })

    def main():
        calls['main'] += 1
        ui.label('main_content')

    def one(idx: int):
        ui.label(f'one-{idx}-{isinstance(idx, int)}')

    def two(idx: str):
        ui.label(f'two-{idx}')

    screen.open('/')
    screen.should_contain('main_content')
    assert screen.current_path == '/'

    screen.click('Go to one')
    screen.should_contain('one-1-True')
    assert screen.current_path == '/one-1'

    screen.click('Go to two')
    screen.should_contain('two-two')
    assert screen.current_path == '/two/two'

    screen.click('Go to wrong match')
    screen.should_not_contain('main_content')
    screen.should_not_contain('one-1-True')
    screen.should_not_contain('two-two')
    screen.should_contain('404: sub page /two-3 not found')
    assert screen.current_path == '/two-3'

    assert calls == {'main': 1}


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
    calls = {'index': 0}

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        calls['index'] += 1
        ui.button('Go', on_click=lambda: ui.navigate.to('/test'))
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

    screen.click('Go')
    screen.should_contain('item: test')

    assert calls == {'index': 1}


def test_navigate_to_new_tab_fallback(screen: Screen):
    """Test that ui.navigate.to with new_tab=True always uses normal navigation."""
    calls = {'index': 0}

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        calls['index'] += 1
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
    assert calls == {'index': 1}

    # NOTE: even though this is a sub page route, new_tab=True should use normal navigation
    screen.click('new tab')
    screen.wait(0.5)
    screen.switch_to(1)
    screen.should_contain('internal-content')
    assert calls == {'index': 2}


def test_adding_sub_pages_after_initialization(screen: Screen):
    @ui.page('/')
    @ui.page('/sub')
    def index():
        pages = ui.sub_pages()
        pages.add('/', lambda: main_content(pages))

    def main_content(pages: ui.sub_pages):
        ui.button('Add sub page', on_click=lambda: pages.add('/sub', sub_content))
        ui.button('Go to sub', on_click=lambda: ui.navigate.to('/sub'))

    def sub_content():
        ui.label('sub-content')

    screen.open('/')
    screen.click('Go to sub')
    screen.should_contain('404: sub page /sub not found')
    assert screen.current_path == '/sub'

    screen.open('/')
    screen.click('Add sub page')
    screen.wait(0.2)
    screen.click('Go to sub')
    screen.should_contain('sub-content')


def test_direct_access_to_sub_page_which_was_added_after_initialization(screen: Screen):
    calls = {'sub_content': 0}

    @ui.page('/')
    @ui.page('/sub')
    def index():
        pages = ui.sub_pages()
        pages.add('/', main_content)
        pages.add('/sub', sub_content)

    def main_content():
        ui.link('Go to sub', '/sub')

    def sub_content():
        calls['sub_content'] += 1
        ui.link('Go to main', '/')

    screen.open('/sub')
    screen.should_contain('Go to main')
    assert calls == {'sub_content': 1}
    assert screen.current_path == '/sub'

    screen.click('Go to main')
    screen.should_contain('Go to sub')
    assert screen.current_path == '/'
    assert calls == {'sub_content': 1}


@pytest.mark.parametrize('page_route', ['/foo/{_:path}', '/foo/sub', '/foo/sub/', '/{_:str}/sub'])
def test_starting_on_non_root_path(screen: Screen, page_route: str):
    @ui.page('/foo')
    @ui.page(page_route)
    def index():
        ui.sub_pages({'/': main_content, '/sub': sub_content}, root_path='/foo')

    def main_content():
        ui.label('main-content')
        ui.link('Go to sub', '/foo/sub')

    def sub_content():
        ui.label('sub-content')
        ui.link('Go to main', '/foo')

    screen.open('/foo/sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'

    screen.click('Go to main')
    screen.should_contain('main-content')
    assert screen.current_path == '/foo'

    screen.click('Go to sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'

    screen.click('Go to main')
    screen.should_contain('main-content')
    assert screen.current_path == '/foo'

    screen.click('Go to sub')
    screen.should_contain('sub-content')
    assert screen.current_path == '/foo/sub'


def test_links_pointing_to_path_which_is_not_a_sub_page(screen: Screen):
    @ui.page('/')
    def index():
        ui.link('Go to main', '/')
        ui.link('Go to sub', '/sub')
        ui.link('Go to other', '/other')
        ui.sub_pages({'/': main, '/sub': sub})

    def main():
        ui.label('main')

    def sub():
        ui.label('sub')

    @ui.page('/other')
    def other():
        ui.label('other page')

    screen.open('/')
    screen.click('Go to sub')
    screen.should_contain('sub')
    assert screen.current_path == '/sub'
    screen.click('Go to other')
    screen.should_contain('other page')
    assert screen.current_path == '/other'


def test_navigate_to_path_which_is_not_a_sub_page(screen: Screen):
    @ui.page('/')
    def index():
        ui.button('Go to main', on_click=lambda: ui.navigate.to('/'))
        ui.button('Go to sub', on_click=lambda: ui.navigate.to('/sub'))
        ui.button('Go to other', on_click=lambda: ui.navigate.to('/other'))
        ui.sub_pages({'/': main, '/sub': sub})

    def main():
        ui.label('main')

    def sub():
        ui.label('sub')

    @ui.page('/other')
    def other():
        ui.label('other page')

    screen.open('/')
    screen.click('Go to sub')
    screen.should_contain('sub')
    assert screen.current_path == '/sub'

    screen.click('Go to other')
    screen.should_contain('other page')
    assert screen.current_path == '/other'


def test_multiple_sub_pages_with_same_path(screen: Screen):
    @ui.page('/')
    def index():
        ui.sub_pages({'/': main, '/other': other})
        ui.sub_pages({'/': main2, '/other': other2})
        ui.link('Go to other', '/other')

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

    screen.click('Go to other')
    screen.should_contain('other content')
    screen.should_contain('other2 content')
    screen.should_not_contain('main content')
    screen.should_not_contain('main2 content')
