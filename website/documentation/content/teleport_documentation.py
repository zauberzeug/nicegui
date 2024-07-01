from nicegui import ui

from . import doc


@doc.demo(ui.teleport)
def main_demo() -> None:
    markdown = ui.markdown('Enter your **name**!')

    def inject_input():
        with ui.teleport(f'#c{markdown.id} strong'):
            ui.input('name').classes('inline-flex').props('dense outlined')

    ui.button('inject input', on_click=inject_input)


@doc.demo('Radio element with arbitrary content', '''
    With the right CSS selector, you can place any content inside a standard radio element.
''')
def arbitrary_content():
    options = ['Star', 'Thump Up', 'Heart']
    radio = ui.radio({x: '' for x in options}, value='Star').props('inline')
    with ui.teleport(f'#c{radio.id} > div:nth-child(1) .q-radio__label'):
        ui.icon('star', size='md')
    with ui.teleport(f'#c{radio.id} > div:nth-child(2) .q-radio__label'):
        ui.icon('thumb_up', size='md')
    with ui.teleport(f'#c{radio.id} > div:nth-child(3) .q-radio__label'):
        ui.icon('favorite', size='md')
    ui.label().bind_text_from(radio, 'value')


doc.reference(ui.teleport)
