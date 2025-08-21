from nicegui import events, ui

from ..windows import browser_window, python_window
from . import (
    add_style_documentation,
    colors_documentation,
    dark_mode_documentation,
    doc,
    element_filter_documentation,
    query_documentation,
)

doc.title('Styling & Appearance')


@doc.demo('Styling', '''
    NiceGUI uses the [Quasar Framework](https://quasar.dev/) and hence has its full design power.
    Each NiceGUI element provides a `props` method whose content is passed [to the Quasar component](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components):
    Have a look at [the Quasar documentation](https://quasar.dev/vue-components/button#design) for all styling props.
    Props with a leading `:` can contain JavaScript expressions that are evaluated on the client.
    You can also apply [Tailwind CSS](https://tailwindcss.com/) utility classes with the `classes` method.

    If you really need to apply CSS, you can use the `style` method. Here the delimiter is `;` instead of a blank space.

    All three functions also provide `remove` and `replace` parameters in case the predefined look is not wanted in a particular styling.
''')
def design_demo():
    ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
    ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
    ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')


doc.text('Try styling NiceGUI elements!', '''
    Try out how
    [Tailwind CSS classes](https://tailwindcss.com/),
    [Quasar props](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components),
    and CSS styles affect NiceGUI elements.
''')


@doc.ui
def styling_demo():
    with ui.row():
        ui.label('Select an element from those available and start styling it!').classes('mx-auto my-auto')
        select_element = ui.select({
            ui.label: 'ui.label',
            ui.checkbox: 'ui.checkbox',
            ui.switch: 'ui.switch',
            ui.input: 'ui.input',
            ui.textarea: 'ui.textarea',
            ui.button: 'ui.button',
        }, value=ui.button, on_change=lambda: live_demo_ui.refresh()).props('dense')

    @ui.refreshable
    def live_demo_ui():
        with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
            with python_window(classes='w-full max-w-[44rem]'):
                with ui.column().classes('w-full gap-2'):
                    ui.markdown(f'''
                        ```py
                        from nicegui import ui

                        element = {select_element.options[select_element.value]}('element')
                        ```
                    ''').classes('mb-[-0.25em]')
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_classes(e: events.ValueChangeEventArguments):
                            try:
                                element.classes(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.classes('`")
                        ui.input(on_change=handle_classes).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_props(e: events.ValueChangeEventArguments):
                            element.props.clear()
                            if isinstance(element, (ui.button, ui.input, ui.textarea)):
                                element.props['label'] = 'element'
                            if isinstance(element, ui.button):
                                element.props['color'] = 'primary'
                            try:
                                element.props(e.value)
                            except ValueError:
                                pass
                            element.update()
                        ui.markdown("`element.props('`")
                        ui.input(on_change=handle_props).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_style(e: events.ValueChangeEventArguments):
                            try:
                                element.style(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.style('`")
                        ui.input(on_change=handle_style).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    ui.markdown('''
                        ```py
                        ui.run()
                        ```
                    ''')
            with browser_window(classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
                element: ui.element = select_element.value('element')
    live_demo_ui()


@doc.demo('Tailwind CSS Layers', '''
    Tailwind CSS' `@layer` directive allows you to define custom classes that can be used in your HTML.
    NiceGUI supports this feature by allowing you to add custom classes to the `components` layer.
    This way, you can define your own classes and use them in your UI elements.
    In the example below, we define a custom class `blue-box` and apply it to two labels.
    Note that the style tag is of type `text/tailwindcss` and not `text/css`.
''')
def tailwind_layers():
    ui.add_head_html('''
        <style type="text/tailwindcss">
            @layer components {
                .blue-box {
                    @apply bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white;
                }
            }
        </style>
    ''')

    with ui.row():
        ui.label('Hello').classes('blue-box')
        ui.label('world').classes('blue-box')


doc.intro(element_filter_documentation)
doc.intro(query_documentation)
doc.intro(colors_documentation)


@doc.demo('CSS Variables', '''
    You can customize the appearance of NiceGUI by setting CSS variables.
    Currently, the following variables with their default values are available:

    - `--nicegui-default-padding: 1rem`
    - `--nicegui-default-gap: 1rem`

''')
def css_variables_demo():
    # ui.add_css('''
    #     :root {
    #         --nicegui-default-padding: 0.5rem;
    #         --nicegui-default-gap: 3rem;
    #     }
    # ''')
    # with ui.card():
    #     ui.label('small padding')
    #     ui.label('large gap')
    # END OF DEMO
    with ui.card().classes('p-[0.5rem] gap-[3rem]'):
        ui.label('small padding')
        ui.label('large gap')


@doc.demo("Overwrite Tailwind's Default Style", '''
    Tailwind resets the default style of HTML elements, like the font size of `h2` elements in this example.
    You can overwrite these defaults by adding a style tag with type `text/tailwindcss`.
    Without this type, the style will be evaluated too early and will be overwritten by Tailwind.
''')
def overwrite_tailwind_style_demo():
    ui.add_head_html('''
        <style type="text/tailwindcss">
            h2 {
                font-size: 150%;
            }
        </style>
    ''')
    ui.html('<h2>Hello world!</h2>')


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
        ui.html('Element Plus button')

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
