import asyncio

from selenium.webdriver.common.by import By

from nicegui import background_tasks, ui
from nicegui.testing import SeleniumScreen


def test_adding_element_to_shared_index_page(screen: SeleniumScreen):
    ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_element_to_private_page(screen: SeleniumScreen):
    @ui.page('/')
    def page():
        ui.button('add label', on_click=lambda: ui.label('added'))

    screen.open('/')
    screen.click('add label')
    screen.should_contain('added')


def test_adding_elements_with_async_await(screen: SeleniumScreen):
    async def add_a():
        await asyncio.sleep(1.0)
        ui.label('A')

    async def add_b():
        await asyncio.sleep(1.0)
        ui.label('B')

    with ui.card() as cardA:
        ui.timer(1.0, add_a, once=True)
    with ui.card() as cardB:
        ui.timer(1.5, add_b, once=True)

    screen.open('/')
    with screen.implicitly_wait(10.0):
        screen.should_contain('A')
        screen.should_contain('B')
    cA = screen.find_element(cardA)
    cA.find_element(By.XPATH, './/*[contains(text(), "A")]')
    cB = screen.find_element(cardB)
    cB.find_element(By.XPATH, './/*[contains(text(), "B")]')


def test_autoupdate_after_connected(screen: SeleniumScreen):
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

    screen.open('/')
    screen.should_contain('before connected')
    screen.should_contain('after connected')
    screen.should_not_contain('one')
    screen.wait_for('one')
    screen.should_not_contain('two')
    screen.wait_for('two')
    screen.should_not_contain('three')
    screen.wait_for('three')


def test_autoupdate_on_async_event_handler(screen: SeleniumScreen):
    async def open_dialog():
        with ui.dialog() as dialog, ui.card():
            label = ui.label('This should be visible')
        dialog.open()
        await asyncio.sleep(1)
        label.text = 'New text after 1 second'
    ui.button('Dialog', on_click=open_dialog)

    screen.open('/')
    screen.click('Dialog')
    screen.should_contain('This should be visible')
    screen.should_not_contain('New text after 1 second')
    screen.should_contain('New text after 1 second')


def test_autoupdate_on_async_timer_callback(screen: SeleniumScreen):
    async def update():
        ui.label('1')
        await asyncio.sleep(1.0)
        ui.label('2')
    ui.label('0')
    ui.button('start', on_click=lambda: ui.timer(2.0, update, once=True))

    screen.open('/')
    screen.click('start')
    screen.should_contain('0')
    screen.should_not_contain('1')
    screen.wait_for('1')
    screen.should_not_contain('2')
    screen.wait_for('2')


def test_adding_elements_from_different_tasks(screen: SeleniumScreen):
    card1 = ui.card()
    card2 = ui.card()

    async def add_label1() -> None:
        with card1:
            await asyncio.sleep(0.5)
            ui.label('1')

    async def add_label2() -> None:
        with card2:
            ui.label('2')
            await asyncio.sleep(0.5)

    ui.timer(0, lambda: ui.label('connection established'), once=True)  # HACK: allow waiting for client connection

    screen.open('/')
    with screen.implicitly_wait(10.0):
        screen.wait_for('connection established')
    background_tasks.create(add_label1())
    background_tasks.create(add_label2())
    screen.should_contain('1')
    screen.should_contain('2')
    c1 = screen.find_element(card1)
    c1.find_element(By.XPATH, './/*[contains(text(), "1")]')
    c2 = screen.find_element(card2)
    c2.find_element(By.XPATH, './/*[contains(text(), "2")]')
