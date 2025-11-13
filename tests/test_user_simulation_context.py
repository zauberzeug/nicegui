import textwrap

import pytest

from nicegui import ui
from nicegui.testing.user_simulation import user_simulation


async def test_user_simulation_script_mode():
    def root():
        ui.button('Click me', on_click=lambda: ui.notify('Hello World!'))

    async with user_simulation(root) as user:
        await user.open('/')
        await user.should_see('Click me')
        user.find(ui.button).click()
        await user.should_see('Hello World!')


async def test_user_simulation_script_mode_with_subpages():
    def root():
        def main():
            ui.label('Main page content')

        def other():
            ui.label('Another page content')

        ui.sub_pages({'/': main, '/other': other})

    async with user_simulation(root) as user:
        await user.open('/')
        await user.should_see('Main')
        await user.open('/other')
        await user.should_see('Another')


async def test_user_simulation_with_page_definitions():
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
async def test_user_simulation_script_main_file(tmp_path, file_content):
    main_path = tmp_path / 'main.py'
    main_path.write_text(file_content, encoding='utf-8')

    async with user_simulation(main_path=main_path) as user:
        await user.open('/')
        await user.should_see('Main file content')


async def test_user_simulation_normal_and_script_mode():
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
