from nicegui.testing import User

# pylint: disable=missing-function-docstring


async def test_checking_items(user: User) -> None:
    await user.open('/')
    await user.should_see('Completed: 1')
    await user.should_see('Remaining: 3')

    user.find('checkbox-new-nicegui-release').click()
    await user.should_see('Completed: 2')
    await user.should_see('Remaining: 2')

    user.find('checkbox-call-mom').click()
    await user.should_see('Completed: 3')
    await user.should_see('Remaining: 1')

    user.find('checkbox-order-pizza').click()
    await user.should_see('Completed: 2')
    await user.should_see('Remaining: 2')


async def test_adding_items(user: User) -> None:
    await user.open('/')

    user.find('new-item') \
        .type('Buy milk').trigger('keydown.enter') \
        .type('Buy eggs').trigger('keydown.enter')
    await user.should_see('Buy milk')
    await user.should_see('Buy eggs')

    user.find('checkbox-buy-milk').click()
    await user.should_see('Completed: 2')
    await user.should_see('Remaining: 4')
