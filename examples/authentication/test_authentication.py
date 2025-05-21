import pytest

from nicegui.testing import User

from . import main

# pylint: disable=missing-function-docstring


@pytest.mark.module_under_test(main)
async def test_login_logoff(user: User) -> None:
    await user.open('/')
    user.find('Username').type('user1')
    user.find('Password').type('pass1')
    user.find('Log in').click()
    await user.should_see('Hello user1!')
    user.find('logout').click()
    await user.should_see('Log in')


@pytest.mark.module_under_test(main)
async def test_wrong_password(user: User) -> None:
    await user.open('/')
    user.find('Username').type('user1')
    user.find('Password').type('wrong').trigger('keydown.enter')
    await user.should_see('Wrong username or password')


@pytest.mark.module_under_test(main)
async def test_subpage_access(user: User) -> None:
    await user.open('/subpage')
    await user.should_see('Log in')
    user.find('Username').type('user1')
    user.find('Password').type('pass1').trigger('keydown.enter')
    await user.should_see('This is a sub page.')
