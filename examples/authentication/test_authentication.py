import pytest

from nicegui.testing import User

from . import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_login_logoff(user: User) -> None:
    await user.open('/')
    await user.type('user1', content='Username')
    await user.type('pass1', content='Password')
    await user.should_see(content='Hello user1!')
    await user.click(content='logout')
    await user.should_see(content='Log in')


@pytest.mark.module_under_test(main)
async def test_wrong_password(user: User) -> None:
    await user.open('/')
    await user.type('user1', content='Username')
    await user.type('wrong', content='Password')
    await user.should_see(content='Wrong username or password')


@pytest.mark.module_under_test(main)
async def test_subpage_access(user: User) -> None:
    await user.open('/subpage')
    await user.should_see(content='Log in')
    await user.type('user1', content='Username')
    await user.type('pass1', content='Password')
    await user.should_see(content='This is a sub page.')
