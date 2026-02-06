import asyncio

from selenium.webdriver.common.by import By

from nicegui import background_tasks, ui
from nicegui.testing import SharedScreen


def test_adding_element_to_shared_index_page(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    shared_screen.open('/')
    shared_screen.click('add label')
    shared_screen.should_contain('added')


def test_adding_element_to_private_page(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    shared_screen.open('/')
    shared_screen.click('add label')
    shared_screen.should_contain('added')


def test_adding_elements_with_async_await(shared_screen: SharedScreen):
    cardA = None
    cardB = None

    @ui.page('/')
    def page():
        async def add_a():
            await asyncio.sleep(1.0)
            ui.label('A')

        async def add_b():
            await asyncio.sleep(1.0)
            ui.label('B')

        nonlocal cardA, cardB
        with ui.card() as cardA:
            ui.timer(1.0, add_a, once=True)
        with ui.card() as cardB:
            ui.timer(1.5, add_b, once=True)

    shared_screen.open('/')
    with shared_screen.implicitly_wait(10.0):
        shared_screen.should_contain('A')
        shared_screen.should_contain('B')
    cA = shared_screen.find_element(cardA)
    cA.find_element(By.XPATH, './/*[contains(text(), "A")]')
    cB = shared_screen.find_element(cardB)
    cB.find_element(By.XPATH, './/*[contains(text(), "B")]')


def test_autoupdate_after_connected(shared_screen: SharedScreen):
    @ui.page('/')
    async def page():
        ui.label('before connected')
        await ui.context.client.connected()
        ui.label('after connected')
        await asyncio.sleep(1)
        ui.label('one')
        await asyncio.sleep(1)
        ui.label('two')
        await asyncio.sleep(1)
        ui.label('three')

    shared_screen.open('/')
    shared_screen.should_contain('before connected')
    shared_screen.should_contain('after connected')
    shared_screen.should_not_contain('one')
    shared_screen.wait_for('one')
    shared_screen.should_not_contain('two')
    shared_screen.wait_for('two')
    shared_screen.should_not_contain('three')
    shared_screen.wait_for('three')


def test_autoupdate_on_async_event_handler(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def open_dialog():
            with ui.dialog() as dialog, ui.card():
                label = ui.label('This should be visible')
            dialog.open()
            await asyncio.sleep(1)
            label.text = 'New text after 1 second'

        ui.button('Dialog', on_click=open_dialog)

    shared_screen.open('/')
    shared_screen.click('Dialog')
    shared_screen.should_contain('This should be visible')
    shared_screen.should_not_contain('New text after 1 second')
    shared_screen.should_contain('New text after 1 second')


def test_autoupdate_on_async_timer_callback(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def update():
            ui.label('1')
            await asyncio.sleep(1.0)
            ui.label('2')
        ui.label('0')
        ui.button('start', on_click=lambda: ui.timer(2.0, update, once=True))

    shared_screen.open('/')
    shared_screen.click('start')
    shared_screen.should_contain('0')
    shared_screen.should_not_contain('1')
    shared_screen.wait_for('1')
    shared_screen.should_not_contain('2')
    shared_screen.wait_for('2')


def test_adding_elements_from_different_tasks(shared_screen: SharedScreen):
    card1 = None
    card2 = None

    @ui.page('/')
    def page():
        nonlocal card1, card2
        card1 = ui.card()
        card2 = ui.card()

        async def add_label1() -> None:
            with card1:
                await asyncio.sleep(0.5)
                ui.label('Label 1')

        async def add_label2() -> None:
            with card2:
                ui.label('Label 2')
                await asyncio.sleep(0.5)

        ui.timer(0, lambda: ui.label('connection established'), once=True)  # HACK: allow waiting for client connection
        ui.button('Add label 1', on_click=lambda: background_tasks.create(add_label1()))
        ui.button('Add label 2', on_click=lambda: background_tasks.create(add_label2()))

    shared_screen.open('/')
    with shared_screen.implicitly_wait(10.0):
        shared_screen.wait_for('connection established')
    shared_screen.click('Add label 1')
    shared_screen.click('Add label 2')
    shared_screen.should_contain('Label 1')
    shared_screen.should_contain('Label 2')
    c1 = shared_screen.find_element(card1)
    c1.find_element(By.XPATH, './/*[contains(text(), "Label 1")]')
    c2 = shared_screen.find_element(card2)
    c2.find_element(By.XPATH, './/*[contains(text(), "Label 2")]')
