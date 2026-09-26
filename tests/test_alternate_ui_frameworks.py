from fastapi.responses import PlainTextResponse

from nicegui import app, ui
from nicegui.testing import Screen

UI_FRAMEWORK_BUNDLE = '''
    window.AlternateUI = {
        install(app) {
            app.component('alt-button', {template: '<button><slot></slot></button>'});
        },
    };
'''


def test_quasar(screen: Screen):
    @ui.page('/')
    def page():
        ui.element('q-btn')

    screen.open('/')
    assert screen.find_by_tag('button')


def test_alternate_framework(screen: Screen):
    @app.get('/alternate-ui.js')
    def alternate_ui():
        return PlainTextResponse(UI_FRAMEWORK_BUNDLE, media_type='text/javascript')

    @ui.page('/')
    def page():
        ui.add_body_html('<script defer src="/alternate-ui.js"></script>')
        app.config.vue_config_script = 'app.use(AlternateUI);'

        ui.element('alt-button')

    screen.open('/')
    assert screen.find_by_tag('button')
