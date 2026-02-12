from nicegui import ui

from .. import doc
from . import (
    add_style_documentation,
    dark_mode_documentation,
)

doc.title('Theming')

doc.intro(dark_mode_documentation)
doc.intro(add_style_documentation)


@doc.demo('Using other Vue UI frameworks', '''
    **This is an experimental feature.**
    **Many NiceGUI elements are likely to break, and the API is subject to change.**

    NiceGUI uses the [Quasar Framework](https://quasar.dev/) by default.
    However, you can also try to use other Vue UI frameworks
    like [Element Plus](https://element-plus.org/en-US/) or [Vuetify](https://vuetifyjs.com/en/).
    To do so, you need to add the framework's JavaScript and CSS file to the head of your HTML document
    and configure NiceGUI accordingly by extending or replacing `app.config.vue_config_script`.

    *Added in NiceGUI 2.21.0*
''')
def other_vue_ui_frameworks_demo():
    from nicegui import app

    # ui.add_body_html('''
    #     <link rel="stylesheet" href="//unpkg.com/element-plus/dist/index.css" />
    #     <script defer src="https://unpkg.com/element-plus"></script>
    # ''')
    # app.config.vue_config_script += '''
    #     app.use(ElementPlus);
    # '''

    with ui.element('el-button').on('click', lambda: ui.notify('Hi!')):
        ui.html('Element Plus button', sanitize=False)

    ui.button('Quasar button', on_click=lambda: ui.notify('Ho!'))

    # END OF DEMO
    ui.add_css('''
        el-button {
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            color: #606266;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            height: 32px;
            line-height: 1;
            padding: 8px 15px;
        }
        el-button:hover {
            background-color: rgb(235.9,245.3,255);
            border-color: rgb(197.7,225.9,255);
            color: rgb(64,158,255);
        }
        el-button:active {
            border-color: rgb(64,158,255);
        }
        body.dark el-button {
            border-color: #4c4d4f;
            color: #cfd3dc;
        }
        body.dark el-button:hover {
            background-color: rgb(24.4, 33.8, 43.5);
            border-color: rgb(33.2, 61.4, 90.5);
            color: rgb(64, 158, 255);
        }
        body.dark el-button:active {
            border-color: rgb(64, 158, 255);
        }
    ''')
