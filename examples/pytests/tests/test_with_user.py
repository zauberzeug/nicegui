from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_markdown_message(user: User) -> None:
    await user.open('/')
    await user.should_see('Try running')


async def test_button_click(user: User) -> None:
    await user.open('/')
    user.find('Click me').click()
    await user.should_see('Button clicked!')


async def test_sub_page(user: User) -> None:
    await user.open('/subpage')
    await user.should_see('This is a subpage')


async def test_with_connected(user: User) -> None:
    await user.open('/with_connected')
    await user.should_see('This is an async connection demo')
    await user.should_see('Connected!')


async def test_navigation(user: User) -> None:
    await user.open('/')
    user.find('go to subpage').click()
    await user.should_see('This is a subpage')
