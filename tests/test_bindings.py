
import pytest
from nicegui import ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .screen import Screen


def test_binding_ui_select_with_tuple_as_key(screen: Screen):
    class Model():
        selection = None
    data = Model()
    options = {
        (1, 1): 'option A',
        (1, 2): 'option B',
    }
    data.selection = list(options.keys())[0]
    ui.select(options).bind_value(data, 'selection')

    screen.open('/')
    screen.should_not_contain('option B')
    element = screen.click('option A')
    screen.click_at_position(element, x=20, y=100)
    screen.wait(0.3)
    screen.should_contain('option B')
