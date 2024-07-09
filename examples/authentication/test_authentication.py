import pytest

from nicegui.testing import User

from . import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_login_logoff(user: User) -> None:
    await user.open('/')
    user.focus('Username').type('user1')
    user.focus('Password').type('pass1')
    user.focus('Log in').click()
    await user.should_see(content='Hello user1!')
    user.focus('logout').click()
    await user.should_see(content='Log in')


@pytest.mark.module_under_test(main)
async def test_wrong_password(user: User) -> None:
    await user.open('/')
    user.focus('Username').type('user1')
    user.focus('Password').type('wrong').trigger('keydown.enter')
    await user.should_see('Wrong username or password')


@pytest.mark.module_under_test(main)
async def test_subpage_access(user: User) -> None:
    await user.open('/subpage')
    await user.should_see('Log in')
    user.focus('Username').type('user1')
    user.focus('Password').type('pass1').trigger('keydown.enter')
    await user.should_see('This is a sub page.')
