from nicegui import app, ui
from nicegui.testing import Screen


def test_quasar(screen: Screen):
    ui.element('q-btn')

    screen.open('/')
    assert screen.find_by_tag('button')


def test_element_plus(screen: Screen):
    ui.add_body_html('<script defer src="https://unpkg.com/element-plus"></script>')
    app.config.vue_config = 'app.use(ElementPlus);'

    ui.element('el-button')

    screen.open('/')
    assert screen.find_by_tag('button')
