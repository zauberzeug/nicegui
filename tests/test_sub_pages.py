import asyncio
from typing import Optional

import pytest

from nicegui import PageArgs, background_tasks, ui
from nicegui.testing import Screen

# pylint: disable=missing-function-docstring


def test_switching_between_sub_pages(screen: Screen):
    calls = {'index': 0, 'a': 0, 'b': 0}

    @ui.page('/')
    @ui.page('/b')
    def index():
        calls['index'] += 1
        ui.label('Index')
        ui.sub_pages({
            '/': sub_page_a,
            '/b': sub_page_b,
        })

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
    screen.should_contain('Page A')
    assert calls == {'index': 1, 'a': 3, 'b': 2}
    screen.click('Go to B with slash')
    screen.should_contain('Page B')
    assert calls == {'index': 1, 'a': 3, 'b': 3}

    screen.click('Go to B with slash')
    screen.should_contain('Page B')
    assert calls == {'index': 1, 'a': 3, 'b': 3}, 'no rebuilding if path stays the same'


def test_passing_data_to_sub_page_via_lambda(screen: Screen):
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


def test_passing_data_to_sub_page_via_dict(screen: Screen):
    @ui.page('/')
    @ui.page('/other')
    def index():
        title = ui.label()
        ui.sub_pages({
            '/': main,
            '/other': other,
        }, data={'title': title})

    def main(title: ui.label):
        title.text = 'main title'
        ui.link('Go to other', '/other')

    def other(args: PageArgs):
        title: ui.label = args.data['title']
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


def test_nested_sub_pages(screen: Screen):
    @ui.page('/')
    @ui.page('/{_:path}')
    def index():
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


def test_async_nested_sub_pages(screen: Screen):
    calls = {
        'index': 0,
        'sleep': 0,
        'sleep_main': 0,
        'background': 0,
        'background_main': 0,
    }

    @ui.page('/')
    @ui.page('/{_:path}')
    def index(_):
        calls['index'] += 1
        ui.link('Go to sleep', '/sleep')
        ui.link('Go to background', '/background')
        ui.sub_pages({
            '/sleep': sleep,
            '/background': background,
        })

    async def sleep():
        calls['sleep'] += 1
        await asyncio.sleep(0.1)
        ui.sub_pages({'/': sleep_main})

    def background():
        async def add():
            await asyncio.sleep(0.05)
            with content:
                ui.sub_pages({'/': background_main})

        calls['background'] += 1
        content = ui.column()
        background_tasks.create(add(), name='lazy_content')

    def sleep_main():
        calls['sleep_main'] += 1
        ui.label('sleep main page')

    def background_main():
        calls['background_main'] += 1
        ui.label('background main page')

    screen.open('/sleep')
    screen.should_contain('sleep main page')
    assert calls == {'index': 1, 'sleep': 1, 'sleep_main': 1, 'background': 0,  'background_main': 0}

    screen.open('/background')
    screen.should_contain('background main page')
    assert calls == {'index': 2, 'sleep': 1, 'sleep_main': 1, 'background': 1, 'background_main': 1}

    screen.click('Go to sleep')
    screen.should_contain('sleep main page')
    assert calls == {'index': 2, 'sleep': 2, 'sleep_main': 2, 'background': 1, 'background_main': 1}

    screen.click('Go to background')
    screen.should_contain('background main page')
    assert calls == {'index': 2, 'sleep': 2, 'sleep_main': 2, 'background': 2, 'background_main': 2}


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
        pages.add('/', main_content)

    def main_content(args: PageArgs):
        ui.button('Add sub page', on_click=lambda: args.frame.add('/sub', sub_content))
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
        ui.label('main page')

    def sub():
        ui.label('sub page')

    @ui.page('/other')
    def other():
        ui.label('other page')

    screen.open('/')
    screen.click('Go to sub')
    screen.should_contain('sub page')
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


@pytest.mark.parametrize('open_with', ['navigate_to', 'link'])
def test_multiple_sub_pages_with_same_path(screen: Screen, open_with: str):
    calls = {'main': 0, 'main2': 0, 'other': 0, 'other2': 0}

    @ui.page('/')
    def index():
        ui.sub_pages({'/': main, '/other': other})
        ui.sub_pages({'/': main2, '/other': other2})
        if open_with == 'navigate_to':
            ui.button('Go to other', on_click=lambda: ui.navigate.to('/other'))
        elif open_with == 'link':
            ui.link('Go to other', '/other')

    def main():
        calls['main'] += 1
        ui.label('main content')

    def main2():
        calls['main2'] += 1
        ui.label('main2 content')

    def other():
        calls['other'] += 1
        ui.label('other content')

    def other2():
        calls['other2'] += 1
        ui.label('other2 content')

    screen.open('/')
    screen.should_contain('main content')
    screen.should_contain('main2 content')
    screen.should_not_contain('other content')
    screen.should_not_contain('other2 content')
    assert calls == {'main': 1, 'main2': 1, 'other': 0, 'other2': 0}

    screen.click('Go to other')
    screen.should_contain('other content')
    screen.should_contain('other2 content')
    screen.should_not_contain('main content')
    screen.should_not_contain('main2 content')
    assert calls == {'main': 1, 'main2': 1, 'other': 1, 'other2': 1}


def test_async_sub_pages(screen: Screen):
    @ui.page('/')
    @ui.page('/{_:path}')
    def index():
        ui.toggle(['/', '/0.1', '/1.0'], value='/', on_change=lambda e: ui.navigate.to(e.value))
        ui.sub_pages({
            '/': main,
            '/{delay}': lambda delay: main(float(delay)),
        })

    async def main(delay: float = 0):
        ui.label(f'waiting for {delay} sec')
        await asyncio.sleep(delay)
        ui.label(f'after {delay} sec')

    screen.open('/')
    screen.should_contain('after 0 sec')

    screen.click('/0.1')
    screen.should_contain('after 0.1 sec')

    # NOTE: below we ensure that quick page changes are not affected by the async sub page
    screen.click('/1.0')
    screen.wait(0.1)
    screen.click('/0.1')
    screen.wait(1)
    screen.should_contain('after 0.1 sec')
    screen.should_not_contain('after 1.0 sec')


@pytest.mark.parametrize('use_page_args', [True, False])
def test_sub_page_with_query_parameters(screen: Screen, use_page_args: bool):
    calls = {'index': 0, 'main_content': 0}

    @ui.page('/')
    def index():
        calls['index'] += 1
        ui.link('Link to main', '/?access=link')
        ui.button('Button to main', on_click=lambda: ui.navigate.to('/?access=button'))
        ui.sub_pages({'/': with_page_args if use_page_args else with_parameter})

    def with_page_args(args: PageArgs):
        calls['main_content'] += 1
        ui.label(f'access: {args.query_parameters["access"]}')

    def with_parameter(access: str):
        calls['main_content'] += 1
        ui.label(f'access: {access}')

    screen.open('/?access=direct')
    screen.should_contain('access: direct')
    assert calls == {'index': 1, 'main_content': 1}

    screen.click('Link to main')
    screen.should_contain('access: link')
    assert calls == {'index': 1, 'main_content': 2}

    screen.click('Button to main')
    screen.should_contain('access: button')
    assert calls == {'index': 1, 'main_content': 3}

    screen.selenium.back()
    screen.should_contain('access: link')
    assert calls == {'index': 1, 'main_content': 4}

    screen.selenium.forward()
    screen.should_contain('access: button')
    assert calls == {'index': 1, 'main_content': 5}


def test_accessing_path_parameters_via_page_args(screen: Screen):
    @ui.page('/')
    @ui.page('/{path:path}')
    def index():
        ui.link('Link with parameter', '/link')
        ui.button('Button with parameter', on_click=lambda: ui.navigate.to('/button'))
        ui.sub_pages({
            '/': main_content,
            '/{parameter}': main_content,
        })

    def main_content(args: PageArgs):
        param = args.path_parameters.get('parameter', 'none')
        ui.label(f'param-{param}')

    screen.open('/')
    screen.should_contain('param-none')

    screen.open('/test')
    screen.should_contain('param-test')

    screen.click('Link with parameter')
    screen.should_contain('param-link')

    screen.click('Button with parameter')
    screen.should_contain('param-button')


def test_optional_parameters(screen: Screen):
    @ui.page('/')
    @ui.page('/{path:path}')
    def index():
        ui.link('Required only', '/test')
        ui.link('With query', '/hello?count=5&active=yes')
        ui.sub_pages({
            '/{name}': content_with_mixed_params,
        }, data={'source': 'data_dict'})

    def content_with_mixed_params(
        name: str,
        count: Optional[int] = 1,
        active: Optional[str] = 'no',
        source: Optional[str] = None,
        missing: Optional[str] = 'default'
    ):
        ui.label(f'name={name}, count={count}, active={active}, source={source}, missing={missing}')

    screen.open('/test')
    screen.should_contain('name=test, count=1, active=no, source=data_dict, missing=default')

    screen.click('With query')
    screen.should_contain('name=hello, count=5, active=yes, source=data_dict, missing=default')


def test_page_args_with_optional_parameters(screen: Screen):

    @ui.page('/')
    @ui.page('/{path:path}')
    def index():
        ui.link('Test PageArgs', '/user/123?role=admin')
        ui.sub_pages({
            '/user/{user_id}': user_page,
        }, data={'app_name': 'MyApp'})

    def user_page(
        args: PageArgs,
        user_id: str,
        role: Optional[str] = 'guest',
        app_name: Optional[str] = None,
    ):
        ui.label(f'path={args.path}, user_id={user_id}, role={role}, app={app_name}')

    screen.open('/')
    screen.click('Test PageArgs')
    screen.should_contain('path=/user/123, user_id=123, role=admin, app=MyApp')


def test_sub_pages_with_url_fragments(screen: Screen):
    calls = {'index': 0, 'main': 0, 'targets': 0}

    @ui.page('/')
    @ui.page('/{_:path}')
    def index():
        calls['index'] += 1
        ui.sub_pages({
            '/': main,
            '/page': targets,
        })

    def main():
        calls['main'] += 1
        ui.label('Main page')
        ui.link('Go to bottom', '/page#bottom')

    def targets():
        calls['targets'] += 1
        ui.link_target('top')
        ui.label('Top target content')
        ui.link('Go to bottom', '/page#bottom')
        for i in range(20):
            ui.label(f'Line {i}').classes('my-5')
        ui.link_target('bottom')
        ui.label('Bottom target content')
        ui.link('Go to top', '/page#top')
        ui.link('Back to main', '/')

    # Test 1: Direct navigation with fragment should work
    screen.open('/page#bottom')
    screen.should_contain('Bottom target content')
    assert screen.current_path == '/page'
    screen.wait(1)
    scroll_y = screen.selenium.execute_script('return window.scrollY')
    assert scroll_y > 500, 'Expected scrolling to occur for fragment navigation'
    assert calls == {'index': 1, 'main': 0, 'targets': 1}

    # Test 2: Same-page fragment navigation should not rebuild pages but should work
    screen.click('Go to top')
    screen.should_contain('Top target content')
    screen.wait(1)
    scroll_y_top = screen.selenium.execute_script('return window.scrollY')
    assert scroll_y_top < scroll_y, 'Expected scrolling to top to have smaller scroll position'
    assert calls == {'index': 1, 'main': 0, 'targets': 1}, 'Fragment navigation should not rebuild page'

    # Test 3: Cross-page navigation with fragment
    screen.click('Back to main')
    screen.should_contain('Main page')
    assert screen.current_path == '/'
    assert calls == {'index': 1, 'main': 1, 'targets': 1}

    # Test 4: Cross-page fragment navigation
    screen.click('Go to bottom')
    screen.should_contain('Bottom target content')
    assert screen.current_path == '/page'
    screen.wait(1)
    scroll_y = screen.selenium.execute_script('return window.scrollY')
    assert scroll_y > 0, 'Expected scrolling after cross-page fragment navigation'
    assert calls == {'index': 1, 'main': 1, 'targets': 2}

    # Test 5: Fragment navigation again
    screen.click('Go to top')
    screen.wait(1)
    assert calls == {'index': 1, 'main': 1, 'targets': 2}, 'Fragment navigation should not rebuild page'


def test_on_path_changed_event(screen: Screen):
    paths = []
    calls = {'index': 0, 'main': 0, 'other': 0}

    @ui.page('/')
    @ui.page('/{_:path}')
    def index():
        calls['index'] += 1
        ui.sub_pages({
            '/': main,
            '/other': other,
        })
        ui.context.client.sub_pages_router.on_path_changed.append(paths.append)
        ui.link('Go to other', '/other')

    def main():
        calls['main'] += 1
        ui.label('main page')

    def other():
        calls['other'] += 1
        ui.label('other page')

    screen.open('/')
    screen.should_contain('main page')
    assert paths == []  # NOTE: initial path is not reported, because the path does not "change" on first load
    assert calls == {'index': 1, 'main': 1, 'other': 0}

    screen.click('Go to other')
    screen.should_contain('other page')
    assert paths == ['/other']
    assert calls == {'index': 1, 'main': 1, 'other': 1}

    screen.open('/other')
    screen.should_contain('other page')
    assert paths == ['/other']
    assert calls == {'index': 2, 'main': 1, 'other': 2}

    screen.open('/bad_path')
    screen.should_contain('404: sub page /bad_path not found')
    assert paths == ['/other']
    assert calls == {'index': 3, 'main': 1, 'other': 2}


def test_shared_client():
    def main():
        ui.label('main page')

    with pytest.raises(AssertionError):
        ui.sub_pages({'/': main, })
