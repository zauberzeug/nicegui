from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from nicegui import ui

from .screen import Screen


def test_keyboard(screen: Screen):
    result = ui.label()
    keyboard = ui.keyboard(on_key=lambda e: result.set_text(f'{e.key, e.action}'))

    screen.open('/')
    assert screen.selenium.find_element(By.ID, keyboard.id)
    ActionChains(screen.selenium) \
        .send_keys('t') \
        .perform()
    screen.should_contain('t, KeyboardAction(keydown=False, keyup=True, repeat=False)')
