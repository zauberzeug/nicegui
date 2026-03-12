from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_login_logoff(user: User) -> None:
    await user.open('/')
    user.find('Username').type('user1')
    user.find('Password').type('pass1')
    user.find('Log in').click()
    await user.should_see('Hello user1!')
    user.find('logout').click()
    await user.should_see('Log in')


async def test_wrong_password(user: User) -> None:
    await user.open('/')
    user.find('Username').type('user1')
    user.find('Password').type('wrong').trigger('keydown.enter')
    await user.should_see('Wrong username or password')


async def test_subpage_access(user: User) -> None:
    await user.open('/subpage')
    await user.should_see('Log in')
    user.find('Username').type('user1')
    user.find('Password').type('pass1').trigger('keydown.enter')
    await user.should_see('This is a sub page.')
