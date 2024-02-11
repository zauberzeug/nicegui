import importlib

import pytest

from nicegui.testing import SimulatedScreen

from .. import main


@pytest.mark.module_under_test(main)
def test_markdown_message(simulated_screen: SimulatedScreen) -> None:
    simulated_screen.open('/')
    simulated_screen.should_contain('Try running')


@pytest.mark.module_under_test(main)
def test_button_click(simulated_screen: SimulatedScreen) -> None:
    simulated_screen.open('/')
    simulated_screen.click('Click me')
    simulated_screen.should_contain('Button clicked!')


@pytest.mark.module_under_test(main)
def test_sub_page(simulated_screen: SimulatedScreen) -> None:
    simulated_screen.open('/subpage')
    simulated_screen.should_contain('This is a subpage')


@pytest.mark.module_under_test(main)
def test_with_connected(simulated_screen: SimulatedScreen) -> None:
    simulated_screen.open('/with_connected')
    simulated_screen.should_contain('This is a subpage')
    simulated_screen.should_contain('Connected!')
