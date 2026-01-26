from nicegui import ui
from nicegui.testing.screen import Screen


def test_caching(screen: Screen):
    @ui.page('/')
    def page():
        ui.markdown('Test **caching**').cache('basic_markdown_cache')

    screen.open('/')
    assert '"hit":false' in screen.selenium.page_source  # Python-land
    assert 'innerHTML":"&lt;p&gt;Test' in screen.selenium.page_source  # JS-land
    screen.should_contain('Test')
    screen.open('/')
    assert '"hit":true' in screen.selenium.page_source  # Python-land
    assert 'innerHTML":"&lt;p&gt;Test' not in screen.selenium.page_source  # JS-land
    screen.should_contain('Test')
