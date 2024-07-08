import asyncio

import pytest

from nicegui.testing import User

from . import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_checking_items(user: User) -> None:
    await user.open('/')
    await user.should_see(content='Completed: 1')
    await user.should_see(content='Remaining: 3')
    await user.click(marker='checkbox-new-nicegui-release')
    await user.should_see(content='Completed: 2')
    await user.should_see(content='Remaining: 2')
    await user.click(marker='checkbox-call-mom')
    await user.should_see(content='Completed: 3')
    await user.should_see(content='Remaining: 1')
    await user.click(marker='checkbox-order-pizza')
    await user.should_see(content='Completed: 2')
    await user.should_see(content='Remaining: 2')


@pytest.mark.module_under_test(main)
async def test_adding_items(user: User) -> None:
    await user.open('/')
    user.focus(marker='new-item') \
        .type('Buy milk').trigger('keydown.enter') \
        .type('Buy eggs').trigger('keydown.enter')
    await user.should_see(content='Buy milk')
    await user.should_see(content='Buy eggs')
    await user.click(marker='checkbox-buy-milk')
    await user.should_see(content='Completed: 2')
    await user.should_see(content='Remaining: 4')
