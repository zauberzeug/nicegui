import asyncio

from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_event_with_update_before_await(screen: Screen):
    @ui.page('/')
    def page():
        async def update():
            ui.label('1')
            await asyncio.sleep(1.0)
            ui.label('2')

        ui.button('update', on_click=update)

    screen.open('/')
    screen.click('update')
    screen.should_contain('1')
    screen.should_not_contain('2')
    screen.should_contain('2')


def test_event_modifiers(screen: Screen):
    events = []
    ui.input('A').on('keydown', lambda _: events.append('A'))
    ui.input('B').on('keydown.x', lambda _: events.append('B'))
    ui.input('C').on('keydown.once', lambda _: events.append('C'))
    ui.input('D').on('keydown.shift.x', lambda _: events.append('D'))

    screen.open('/')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="A"]').send_keys('x')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="B"]').send_keys('xy')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="C"]').send_keys('xx')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="D"]').send_keys('Xx')
    assert events == ['A', 'B', 'C', 'D']
