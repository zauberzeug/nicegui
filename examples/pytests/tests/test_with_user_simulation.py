
import pytest

from nicegui.testing import User

from .. import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_markdown_message(user: User) -> None:
    await user.open('/')
    await user.should_see('Try running')


@pytest.mark.module_under_test(main)
async def test_button_click(user: User) -> None:
    await user.open('/')
    user.focus('Click me').click()
    await user.should_see('Button clicked!')


@pytest.mark.module_under_test(main)
async def test_sub_page(user: User) -> None:
    await user.open('/subpage')
    await user.should_see('This is a subpage')


@pytest.mark.module_under_test(main)
async def test_with_connected(user: User) -> None:
    await user.open('/with_connected')
    await user.should_see('This is an async connection demo')
    await user.should_see('Connected!')


@pytest.mark.module_under_test(main)
async def test_navigation(user: User) -> None:
    await user.open('/')
    user.focus(content='go to subpage').click()
    await user.should_see('This is a subpage')
