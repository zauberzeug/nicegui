from nicegui import ui

from .user import User


async def test_title(user: User):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('some content')

    user.open()
    user.should_see('My Custom Title')


async def test_route_with_custom_path(user: User):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')

    user.open('/test_route')
    user.should_see('page with custom path')


async def test_link_to_page_by_passing_function(user: User):
    @ui.page('/subpage')
    def page():
        ui.label('the subpage')

    ui.link('link to subpage', page)

    user.open()
    user.click('link to subpage')
    user.should_see('the subpage')
