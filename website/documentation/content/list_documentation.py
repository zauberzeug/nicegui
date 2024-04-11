from nicegui import ui

from . import doc


@doc.demo(ui.list)
def main_demo() -> None:
    with ui.list().props('dense separator'):
        ui.item('3 Apples')
        ui.item('5 Bananas')
        ui.item('8 Strawberries')
        ui.item('13 Walnuts')


@doc.demo('Items, Sections and Labels', '''
    List items use item sections to structure their content.
    Item labels take different positions depending on their props.
''')
def contact_list():
    with ui.list().props('bordered separator'):
        ui.item_label('Contacts').props('header').classes('text-bold')
        ui.separator()
        with ui.item(on_click=lambda: ui.notify('Selected contact 1')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('Nice Guy')
                ui.item_label('name').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')
        with ui.item(on_click=lambda: ui.notify('Selected contact 2')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('Nice Person')
                ui.item_label('name').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')


doc.reference(ui.list, title='Reference for ui.list')
doc.reference(ui.item, title='Reference for ui.item')
doc.reference(ui.item_section, title='Reference for ui.item_section')
doc.reference(ui.item_label, title='Reference for ui.item_label')
