import asyncio
from typing import Generator

from nicegui import ui
from nicegui.task_logger import create_task

from .screen import Screen


def test_adding_element_to_shared_index_page(screen: Screen):
    ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_element_to_private_page(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_elements_with_async_await(screen: Screen):
    async def add_a():
        await asyncio.sleep(0.1)
        ui.label('A')

    async def add_b():
        await asyncio.sleep(0.1)
        ui.label('B')

    with ui.card():
        ui.timer(1.0, add_a, once=True)
    with ui.card():
        ui.timer(1.1, add_b, once=True)

    # TODO
    # screen.open('/')
    # for _ in range(100):
    #     if '    card\n      A\n    card\n      B' in screen.render_content():
    #         return
    #     screen.wait(0.1)
    # raise AssertionError(f'{screen.render_content()} should show cards with "A" and "B"')


def test_adding_elements_during_onconnect(screen: Screen):
    ui.label('Label 1')
    ui.on_connect(lambda: ui.label('Label 2'))

    screen.open('/')
    screen.should_contain('Label 2')


def test_autoupdate_on_async_page_after_yield(screen: Screen):
    @ui.page('/')
    async def page() -> Generator[None, PageEvent, None]:
        ui.label('before page is ready')
        yield
        ui.label('page ready')
        await asyncio.sleep(1)
        ui.label('one')
        await asyncio.sleep(1)
        ui.label('two')
        await asyncio.sleep(1)
        ui.label('three')

    screen.open('/')
    screen.should_contain('before page is ready')
    screen.should_contain('page ready')
    screen.should_not_contain('one')
    screen.wait_for('one')
    screen.should_not_contain('two')
    screen.wait_for('two')
    screen.should_not_contain('three')
    screen.wait_for('three')


def test_autoupdate_on_async_page_ready_callback(screen: Screen):
    async def ready():
        ui.label('page ready')
        await asyncio.sleep(1)
        ui.label('after delay')

    @ui.page('/', on_page_ready=ready)
    def page() -> Generator[None, PageEvent, None]:
        ui.label('before page is ready')

    screen.open('/')
    screen.should_contain('before page is ready')
    screen.should_contain('page ready')
    screen.should_not_contain('after delay')
    screen.wait_for('after delay')


def test_autoupdate_on_async_event_handler(screen: Screen):
    async def open():
        with ui.dialog() as dialog, ui.card():
            l = ui.label('This should be visible')
        dialog.open()
        await asyncio.sleep(1)
        l.text = 'New text after 1 second'
    ui.button('Dialog', on_click=open)

    screen.open('/')
    screen.click('Dialog')
    screen.should_contain('This should be visible')
    screen.should_not_contain('New text after 1 second')
    screen.wait_for('New text after 1 second')


def test_autoupdate_on_async_timer_callback(screen: Screen):
    async def update():
        ui.label('1')
        await asyncio.sleep(1.0)
        ui.label('2')
    ui.timer(2.0, update, once=True)

    screen.open('/')
    screen.should_not_contain('1')
    screen.wait_for('1')
    screen.should_not_contain('2')
    screen.wait_for('2')


def test_adding_elements_from_different_tasks(screen: Screen):
    card1 = ui.card()
    card2 = ui.card()

    async def add_label1() -> None:
        with card1:
            await asyncio.sleep(1.0)
            ui.label('1')

    async def add_label2() -> None:
        with card2:
            ui.label('2')
            await asyncio.sleep(1.0)

    screen.open('/')
    create_task(add_label1())
    create_task(add_label2())
    screen.wait_for('1')
    screen.wait_for('2')
    # TODO
#     assert screen.render_content() == '''Title: NiceGUI

#     card
#       1
#     card
#       2
# '''
