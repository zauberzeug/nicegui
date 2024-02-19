from nicegui import ElementFilter, ui

from . import doc


@doc.demo(ElementFilter)
def main_demo() -> None:
    from nicegui import ElementFilter

    with ui.row():
        ui.button('button A')
        ui.label('label A')
    with ui.row().mark('important'):
        ui.button('button B')
        ui.label('label B')

    ElementFilter(kind=ui.label).within(marker='important').classes('text-xl')


@doc.demo('Find all elements with text property', '''
    The `text` property is provided by a mixin called `TextElement`.
    If we filter by such a mixin the ElementFilter itself will provide a typed iterable.
''')
def text_element() -> None:
    from nicegui import ElementFilter
    from nicegui.elements.mixins.text_element import TextElement

    with ui.row():
        ui.button('button')
        ui.icon('home')
        ui.label('label A')
        ui.label('label B')

    # ui.label(', '.join([b.text for b in ElementFilter(kind=TextElement)]))
    # END OF DEMO
    ui.label(', '.join([b.text for b in ElementFilter(kind=TextElement, local_scope=True)]))
