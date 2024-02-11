import asyncio
import importlib

from nicegui.testing import SimulatedScreen

from .. import main


def test_markdown_message(simulated_screen: SimulatedScreen) -> None:
    importlib.reload(main)

    simulated_screen.open('/')
    simulated_screen.should_contain('Try running')


def test_button_click(simulated_screen: SimulatedScreen) -> None:
    importlib.reload(main)

    simulated_screen.open('/')
    simulated_screen.click('Click me')
    simulated_screen.should_contain('Button clicked!')


def test_sub_page(simulated_screen: SimulatedScreen) -> None:
    importlib.reload(main)

    simulated_screen.open('/subpage')
    simulated_screen.should_contain('This is a subpage')


def test_with_connected(simulated_screen: SimulatedScreen) -> None:
    importlib.reload(main)

    simulated_screen.open('/with_connected')
    simulated_screen.should_contain('This is a subpage')
    simulated_screen.should_contain('Connected!')
