from nicegui import app, ui
from nicegui.testing import SharedScreen


def test_quasar(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.element('q-btn')

    shared_screen.open('/')
    assert shared_screen.find_by_tag('button')


def test_element_plus(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.add_body_html('<script defer src="https://unpkg.com/element-plus"></script>')
        app.config.vue_config_script = 'app.use(ElementPlus);'

        ui.element('el-button')

    shared_screen.open('/')
    assert shared_screen.find_by_tag('button')
