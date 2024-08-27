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
                element: ui.element = select_element.value('element')
    live_demo_ui()


@doc.demo('Tailwind CSS', '''
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
