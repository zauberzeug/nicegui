import importlib

from nicegui.testing import SimulatedScreen

from .. import main


def test_quick(simulated_screen: SimulatedScreen) -> None:
    importlib.reload(main)

    simulated_screen.open('/')
    simulated_screen.should_contain('Try running')
