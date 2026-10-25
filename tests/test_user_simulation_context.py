import asyncio
import gc
import textwrap
from pathlib import Path

import pytest

from nicegui import ui
from nicegui.testing.user_simulation import user_simulation


async def test_basic_root_function():
    def root():
        ui.button('Click me', on_click=lambda: ui.notify('Hello World!'))

    async with user_simulation(root) as user:
        await user.open('/')
        await user.should_see('Click me')

        user.find(ui.button).click()
        await user.should_see('Hello World!')


async def test_root_function_with_subpages():
    def root():
        ui.sub_pages({'/': main, '/other': other})

    def main():
        ui.label('Main page content')

    def other():
        ui.label('Another page content')

    async with user_simulation(root) as user:
        await user.open('/')
        await user.should_see('Main')

        await user.open('/other')
        await user.should_see('Another')


async def test_with_page_definitions():
    async with user_simulation() as user:

        @ui.page('/')
        def page():
            ui.label('Main page')

        @ui.page('/a')
        def pageA():
            ui.label('Page A')

        await user.open('/')
        await user.should_see('Main page')

        await user.open('/a')
        await user.should_see('Page A')


@pytest.mark.parametrize('file_content', [
    textwrap.dedent('''
        from nicegui import ui

        @ui.page("/")
        def page():
            ui.label("Main file content")

        ui.run()
    '''),
    textwrap.dedent('''
        from nicegui import ui

        def root():
            ui.label("Main file content")

        ui.run(root)
    '''),
])
async def test_main_file(tmp_path: Path, file_content: str):
    main_file = tmp_path / 'main.py'
    main_file.write_text(file_content, encoding='utf-8')

    async with user_simulation(main_file=main_file) as user:
        await user.open('/')
        await user.should_see('Main file content')


async def test_earlier_runs_of_main_file_are_freed(tmp_path: Path):
    main_file = tmp_path / 'main.py'
    main_file.write_text(textwrap.dedent('''
        from fastapi.responses import PlainTextResponse
        from nicegui import app, ui

        class Greeting(ui.label):
            pass

        class NotFound(Exception):
            pass

        @app.exception_handler(NotFound)
        async def handle_not_found(request, error):
            return PlainTextResponse(str(error), status_code=404)

        @ui.page("/")
        def page():
            Greeting("Main file content")

        ui.run()
    '''), encoding='utf-8')

    async def count_greeting_classes() -> int:
        async with user_simulation(main_file=main_file) as user:
            await user.open('/')
            await user.should_see('Main file content')
            gc.collect()
            return [cls.__name__ for cls in ui.label.__subclasses__()].count('Greeting')

    # Like separate tests, each simulation runs in its own task, so the request kept in a context variable ends with it.
    assert [await asyncio.create_task(count_greeting_classes()) for _ in range(3)] == [1, 1, 1]


async def test_adding_page_to_root_function():
    def root():
        ui.button('Click me', on_click=lambda: ui.notify('Hello World!'))

    async with user_simulation(root) as user:
        @ui.page('/a')
        def pageA():
            ui.label('Page A')

        await user.open('/')
        await user.should_see('Click me')

        user.find(ui.button).click()
        await user.should_see('Hello World!')

        await user.open('/a')
        await user.should_see('Page A')


@pytest.mark.parametrize('_first_run', [True, False])
async def test_main_file_with_submodule_pages(tmp_path: Path, _first_run: bool):
    (pages_dir := tmp_path / 'pages').mkdir()
    (pages_dir / '__init__.py').write_text('from .dashboard import dashboard_page')
    (pages_dir / 'dashboard.py').write_text(textwrap.dedent('''
        from nicegui import ui
        @ui.page('/dashboard')
        def dashboard_page():
            ui.label('Dashboard Content')
    '''))

    main_file = tmp_path / 'main.py'
    main_file.write_text(textwrap.dedent('''
        import sys
        sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
        import pages
        from nicegui import ui
        ui.run()
    '''))

    async with user_simulation(main_file=main_file) as user:
        await user.open('/dashboard')
        await user.should_see('Dashboard Content')
