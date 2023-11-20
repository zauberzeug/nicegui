from nicegui import events, ui

from ..demo import browser_window, python_window
from ..tools import load_demo, subheading, text_demo

name = 'styling_appearance'
title = 'Styling & Appearance'
description = '''
    NiceGUI allows to customize the appearance of UI elements in various ways, including CSS, Tailwind CSS and Quasar properties.
'''


def content() -> None:
    @text_demo('Styling', '''
        NiceGUI uses the [Quasar Framework](https://quasar.dev/) version 1.0 and hence has its full design power.
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

    subheading('Try styling NiceGUI elements!')
    ui.markdown('''
        Try out how
        [Tailwind CSS classes](https://tailwindcss.com/),
        [Quasar props](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components),
        and CSS styles affect NiceGUI elements.
    ''').classes('bold-links arrow-links mb-[-1rem]')
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
                with ui.column().classes('w-full gap-4'):
                    ui.markdown(f'''
                        ```py
                        from nicegui import ui

                        element = {select_element.options[select_element.value]}('element')
                        ```
                    ''').classes('mb-[-0.25em]')
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_classes(e: events.ValueChangeEventArguments):
                            try:
                                element.classes(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.classes('`")
                        ui.input(on_change=handle_classes).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_props(e: events.ValueChangeEventArguments):
                            element._props = {'label': 'Button', 'color': 'primary'}
                            try:
                                element.props(e.value)
                            except ValueError:
                                pass
                            element.update()
                        ui.markdown("`element.props('`")
                        ui.input(on_change=handle_props).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full px-2'):
                        def handle_style(e: events.ValueChangeEventArguments):
                            try:
                                element.style(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.style('`")
                        ui.input(on_change=handle_style).classes('mt-[-0.5em] text-mono grow').props('dense')
                        ui.markdown("`')`")
                    ui.markdown('''
                        ```py
                        ui.run()
                        ```
                    ''')
            with browser_window(classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
                element: ui.element = select_element.value("element")
    live_demo_ui()

    @text_demo('Tailwind CSS', '''
        [Tailwind CSS](https://tailwindcss.com/) is a CSS framework for rapidly building custom user interfaces.
        NiceGUI provides a fluent, auto-complete friendly interface for adding Tailwind classes to UI elements.
        
        You can discover available classes by navigating the methods of the `tailwind` property.
        The builder pattern allows you to chain multiple classes together (as shown with "Label A").
        You can also call the `tailwind` property with a list of classes (as shown with "Label B").

        Although this is very similar to using the `classes` method, it is more convenient for Tailwind classes due to auto-completion.

        Last but not least, you can also predefine a style and apply it to multiple elements (labels C and D).
               
        Note that sometimes Tailwind is overruled by Quasar styles, e.g. when using `ui.button('Button').tailwind('bg-red-500')`.
        This is a known limitation and not fully in our control.
        But we try to provide solutions like the `color` parameter: `ui.button('Button', color='red-500')`.
    ''')
    def tailwind_demo():
        from nicegui import Tailwind
        ui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')
        ui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')

        red_style = Tailwind().text_color('red-600').font_weight('bold')
        label_c = ui.label('Label C')
        red_style.apply(label_c)
        ui.label('Label D').tailwind(red_style)

    load_demo(ui.query)
    load_demo(ui.colors)
    load_demo(ui.dark_mode)
