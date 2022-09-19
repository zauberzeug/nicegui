from nicegui import ui


async def test_title(user):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('some content')
    user.open()
    user.should_see('My Custom Title')


async def test_route_with_custom_path(user):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')
    user.open('/test_route')
    user.should_see('page with custom path')
