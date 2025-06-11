from nicegui import app, ui
from nicegui.testing import Screen


def test_element_plus(screen: Screen):
    ui.add_body_html('''
    <link rel="stylesheet" href="//unpkg.com/element-plus/dist/index.css" />
    <script defer src="//unpkg.com/element-plus"></script>
    ''', shared=True)

    app.configure_vue_ui_framework('''
    app.use(ElementPlus);
    ''')

    with ui.element('el-button'):
        ui.html('I am a button from Element Plus')

    screen.open('/')
    assert len(screen.find_all_by_tag('el-button')) == 0, 'Some el-button tags indicate that Element Plus is not loaded'
    assert len(screen.find_all_by_tag('button')) == 1, 'No button tag found, Element Plus is not loaded'


def test_quasar(screen: Screen):
    with ui.element('q-btn'):
        ui.html('I am a button from Quasar')

    screen.open('/')
    assert len(screen.find_all_by_tag('q-btn')) == 0, 'Some q-btn tags indicate that Quasar is not loaded'
    assert len(screen.find_all_by_tag('button')) == 1, 'No button tag found, Quasar is not loaded'
