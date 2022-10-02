
import pytest
from nicegui import ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .screen import Screen


def test_binding_ui_select_with_tuple_as_key(screen: Screen):
    class Model():
        location = None
    data = Model()
    options = {
        (51.9607, 7.6261): 'option A',
        (48.3069, 14.2858): 'option B',
    }
    data.location = list(options.keys())[0]
    ui.select(options).bind_value(data, 'location')

    screen.open('/')
    screen.should_not_contain('option B')
    element = screen.click('option A')
    screen.click_at_position(element, x=20, y=100)
    screen.wait(0.3)
    screen.should_contain('option B')
