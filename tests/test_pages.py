from nicegui import ui


async def test_title(server, selenium):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('hello world')
    server.start()
    selenium.get(server.base_url)
    assert "My Custom Title" in selenium.title
