from nicegui import ui

from . import (
    colors_documentation,
    doc,
    element_filter_documentation,
    query_documentation,
)

doc.title('Selectors & Colors')

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
    Tailwind CSS resets the default style of HTML elements, like the font size of `h2` elements in this example.
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
    ui.html('<h2>Hello world!</h2>', sanitize=False)
