
import pytest

from nicegui.testing import SimulatedScreen

from .. import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_markdown_message(screen: SimulatedScreen) -> None:
    with await screen.open('/'):
        await screen.should_contain('Try running')


@pytest.mark.module_under_test(main)
async def test_button_click(screen: SimulatedScreen) -> None:
    with await screen.open('/'):
        screen.click('Click me')
        await screen.should_contain('Button clicked!')


@pytest.mark.module_under_test(main)
async def test_sub_page(screen: SimulatedScreen) -> None:
    with await screen.open('/subpage'):
        await screen.should_contain('This is a subpage')


@pytest.mark.module_under_test(main)
async def test_with_connected(screen: SimulatedScreen) -> None:
    with await screen.open('/with_connected'):
        await screen.should_contain('This is an async connection demo')
        await screen.should_contain('Connected!')
