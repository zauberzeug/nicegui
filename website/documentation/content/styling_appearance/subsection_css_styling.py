from nicegui import events, ui

from ...windows import browser_window, python_window
from .. import doc

doc.title('CSS Styling')


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


doc.text('', '''
    **How to overrule Quasar with Tailwind classes or plain CSS**

    Some Quasar classes (e.g. `bg-primary`) are marked as `!important` and, thus, would even overrule `!important` Tailwind classes.
    At NiceGUI, we deviate from Quasar's design by moving Quasar's `!important` styles to a less powerful CSS layer.
    While still important enough to ensure Quasar works as expected, you can now overrule Quasar for more customization.

    Try out class `!bg-red-500` on a `ui.button` to see important Tailwind classes overruling Quasar.
    Similarly, you can set the style `background-color:red !important` to achieve the same effect.
''')


@doc.demo('CSS Layers', '''
    NiceGUI defines the following CSS layers (in order of increasing priority):
    "theme", "base", "quasar", "nicegui", "components", "utilities", "overrides", and "quasar_importants".

    You don't need to put your custom CSS into layers for basic styling.
    However, to override Quasar's `!important` rules, you should define your CSS in an appropriate layer:
    use "components" for component-specific styles or "utilities" for utility classes,
    depending on the purpose of your custom styles.
    Note that you need to use `!important` in your custom styles
    because Quasar defines most of its CSS with `!important`,
    which would otherwise take precedence.

    In the example below, we override a button's background color using the "utilities" layer.

    *Updated in NiceGUI 3.0.0: CSS layers have been introduced.*
''')
def css_layers():
    ui.add_css('''
        @layer utilities {
           .red-background {
               background-color: red !important;
            }
        }
    ''')
    ui.button('Red Button').classes('red-background')


@doc.demo('Tailwind CSS Layers', '''
    Tailwind CSS' `@layer` directive allows you to define custom classes that can be used in your HTML.
    NiceGUI supports this feature by allowing you to add custom classes to the `components` layer.
    This way, you can define your own classes and use them in your UI elements.
    In the example below, we define a custom class `blue-box` and apply it to two labels.
    Note that the style tag is of type `text/tailwindcss` and not `text/css`.

    Also note: This requires the default Tailwind CSS engine (not UnoCSS).
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
        # ui.label('Hello').classes('blue-box')
        # ui.label('world').classes('blue-box')
        # END OF DEMO
        ui.label('Hello').classes('bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white')
        ui.label('world').classes('bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white')


@doc.demo('UnoCSS engine', '''
    As an alternative to using the [Tailwind CSS Play CDN engine](https://v3.tailwindcss.com/docs/installation/play-cdn),
    you can also use the [UnoCSS engine](https://unocss.dev/) to let Tailwind CSS classes take effect.

    Pass one of the following presets to `ui.run(unocss=...)`:

    - "mini": [UnoCSS Mini preset](https://unocss.dev/presets/mini)
    - "wind3": [UnoCSS Wind3 preset](https://unocss.dev/presets/wind3)
    - "wind4": [UnoCSS Wind4 preset](https://unocss.dev/presets/wind4)

    UnoCSS is a smaller library and more performant, especially on small pages.
    In Lighthouse Desktop, load time for this page went from 1.1s down to 0.7s.

    However, full compatibility with Tailwind CSS is not guaranteed.
    For example, Tailwind CSS Layers (see above) do not work with UnoCSS.

    *Added in NiceGUI 3.7.0*
''')
def unocss_demo():
    label = ui.label('This label becomes red dynamically.')

    ui.button('Become red', on_click=lambda: ui.run_javascript(f'''
        {label.html_id}.classList.add("text-red-500")
    '''))

    # ui.run(unocss='mini')
