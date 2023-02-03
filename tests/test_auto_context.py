import asyncio

from selenium.webdriver.common.by import By

from nicegui import Client, background_tasks, ui

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

    with ui.card() as cardA:
        ui.timer(1.0, add_a, once=True)
    with ui.card() as cardB:
        ui.timer(1.1, add_b, once=True)

    screen.open('/')
    screen.should_contain('A')
    screen.should_contain('B')
    cA = screen.selenium.find_element(By.ID, cardA.id)
    cA.find_element(By.XPATH, './/*[contains(text(), "A")]')
    cB = screen.selenium.find_element(By.ID, cardB.id)
    cB.find_element(By.XPATH, './/*[contains(text(), "B")]')


def test_autoupdate_after_connected(screen: Screen):
    @ui.page('/')
    async def page(client: Client):
        ui.label('before connected')
        await client.connected()
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
    screen.should_contain('New text after 1 second')


def test_autoupdate_on_async_timer_callback(screen: Screen):
    async def update():
        ui.label('1')
        await asyncio.sleep(2.0)
        ui.label('2')
    ui.label('0')
    ui.timer(2.0, update, once=True)

    screen.open('/')
    screen.should_contain('0')
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
    background_tasks.create(add_label1())
    background_tasks.create(add_label2())
    screen.should_contain('1')
    screen.should_contain('2')
    c1 = screen.selenium.find_element(By.ID, card1.id)
    c1.find_element(By.XPATH, './/*[contains(text(), "1")]')
    c2 = screen.selenium.find_element(By.ID, card2.id)
    c2.find_element(By.XPATH, './/*[contains(text(), "2")]')
