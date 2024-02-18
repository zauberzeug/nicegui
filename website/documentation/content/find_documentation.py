from nicegui import ui

from . import doc


@doc.demo(ui.find)
def main_demo() -> None:
    with ui.row():
        ui.button('button A')
        ui.label('label A')
    with ui.row().keys('important'):
        ui.button('button B')
        ui.label('label B').classes('text-xl')  # HIDE

    ui.find(type=ui.label).within(key='important').classes('text-2xl')


@doc.demo('Find all elements with text property', '''
    The `text` property is provided by a mixin called `TextElement`.
    All elements that have a text property are also of type `TextElement` and hence can be filtered by this type.
''')
def text_element() -> None:
    from nicegui.elements.mixins.text_element import TextElement

    with ui.row():
        ui.button('button')
        ui.icon('home')
        ui.label('label A')
        ui.label('label B')

    # ui.label(', '.join([b.text for b in ui.get(type=TextElement)]))
    # END OF DEMO
    ui.label(', '.join([b.text for b in ui.find(type=TextElement, local_scope=True)]))
