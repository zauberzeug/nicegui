from textwrap import dedent

from website.documentation.code_extraction import get_full_code, transform_for_demo_execution


def prepare(text: str) -> str:
    return dedent(text).strip() + '\n'


def test_simple_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({'/': main, '/other': other})

        ui.run(root)
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {'/': main, '/other': other}
            pages.init()

        ui.run(root)
    ''')


def test_sub_pages_with_data():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({
                '/': main,
                '/other': other,
            }, data={'title': title})
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {
                '/': main,
                '/other': other,
            }
            pages.data = {'title': title}
            pages.init()
    ''')


def test_empty_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            pages = ui.sub_pages()
            pages.add('/', main)
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.init()
            pages.add('/', main)
    ''')


def test_chained_methods():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({
                '/': main,
                '/other': other,
            }).classes('border p-2')
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {
                '/': main,
                '/other': other,
            }
            pages.classes('border p-2')
            pages.init()
    ''')


def test_ui_link_transformation():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.link('Home', '/')
            ui.sub_pages({'/': main})
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.link('Home', '/')
            pages.routes = {'/': main}
            pages.init()
    ''')


def test_ui_link_before_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.link('msg=hello', '/?msg=hello')
            ui.link('msg=world', '/?msg=world')
            ui.sub_pages({'/': main})
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.link('msg=hello', '/?msg=hello')
            pages.link('msg=world', '/?msg=world')
            pages.routes = {'/': main}
            pages.init()
    ''')


def test_multiple_imports():
    assert transform_for_demo_execution(prepare('''
        from nicegui import PageArguments, ui

        def root():
            ui.link('test', '/')
            ui.sub_pages({'/': main})
    ''')) == prepare('''
        from nicegui import PageArguments, ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.link('test', '/')
            pages.routes = {'/': main}
            pages.init()
    ''')


def test_nested_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({'/': main, '/other': other})

        def other():
            ui.link('Go to A', '/other/a') # TRANSFORM: nested '/a'
            ui.sub_pages({'/': sub_main}) # TRANSFORM: nested
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {'/': main, '/other': other}
            pages.init()

        def other():
            nested = FakeSubPages()
            nested.link('Go to A', '/a')
            nested.routes = {'/': sub_main}
            nested.init()
    ''')


def test_no_transformation_without_sub_pages():
    code = prepare('''
        from nicegui import ui

        def root():
            ui.label('Hello')
            ui.button('Click me')
    ''')
    assert transform_for_demo_execution(code) == code


def test_single_line_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({'/': main})
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {'/': main}
            pages.init()
    ''')


def test_multiline_sub_pages():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.sub_pages({
                '/': main,
                '/about': lambda: other('About'),
                '/contact': contact,
            }, data={'foo': 'bar'})
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.routes = {
                '/': main,
                '/about': lambda: other('About'),
                '/contact': contact,
            }
            pages.data = {'foo': 'bar'}
            pages.init()
    ''')


def test_transform_hint():
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.link('item 1', '/item/1')  # TRANSFORM: pages '/item/{item_id}', item_id=1
            ui.link('item 2', '/item/2')  # TRANSFORM: pages '/item/{item_id}', item_id=2
            ui.sub_pages({'/': main, '/item/{item_id}': item})

        ui.run(root)
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.link('item 1', '/item/{item_id}', item_id=1)
            pages.link('item 2', '/item/{item_id}', item_id=2)
            pages.routes = {'/': main, '/item/{item_id}': item}
            pages.init()

        ui.run(root)
    ''')


def test_hide_directive_with_comment():
    """Test that # HIDE can be used to show one version in display and execute another."""
    assert transform_for_demo_execution(prepare('''
        from nicegui import ui

        def root():
            ui.link('test', '/')
            ui.sub_pages({'/': main})

        # def main(args: PageArguments):
        def main(args: PageArguments = FakeArguments(msg='no message')):  # HIDE
            ui.label(args.query_parameters.get('msg', 'no message'))
    ''')) == prepare('''
        from nicegui import ui
        from website.documentation.content.sub_pages_documentation import FakeArguments, FakeSubPages

        pages = FakeSubPages()

        def root():
            pages.link('test', '/')
            pages.routes = {'/': main}
            pages.init()

        def main(args: PageArguments = FakeArguments(msg='no message')):
            ui.label(args.query_parameters.get('msg', 'no message'))
    ''')


def test_get_full_code_with_hide_and_comment():
    """Test that get_full_code shows commented line and hides the HIDE line for display."""
    def demo_func():
        from nicegui import ui

        def _root():
            ui.sub_pages({'/': main})

        # def main():
        def main():  # HIDE
            ui.label('test')

    display_code = get_full_code(demo_func, keep_transform=False)
    assert 'def main():' in display_code
    assert '# HIDE' not in display_code
    assert display_code.count('def main():') == 1

    execution_code = get_full_code(demo_func, keep_transform=True)
    assert '# def main():' in execution_code
    assert 'def main():  # HIDE' in execution_code
