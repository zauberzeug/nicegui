
import pytest

from nicegui.testing import User

from .. import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_markdown_message(user: User) -> None:
    await user.open('/')
    await user.should_see(content='Try running')


@pytest.mark.module_under_test(main)
async def test_button_click(user: User) -> None:
    await user.open('/')
    await user.click(content='Click me')
    await user.should_see(content='Button clicked!')


@pytest.mark.module_under_test(main)
async def test_sub_page(user: User) -> None:
    await user.open('/subpage')
    await user.should_see(content='This is a subpage')


@pytest.mark.module_under_test(main)
async def test_with_connected(user: User) -> None:
    await user.open('/with_connected')
    await user.should_see(content='This is an async connection demo')
    await user.should_see(content='Connected!')
