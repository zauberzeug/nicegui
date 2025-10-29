from nicegui import ui
from nicegui.elements.radio import Radio

from . import doc


@doc.demo(Radio)
def main_demo() -> None:
    radio1 = ui.radio([1, 2, 3], value=1).props('inline')
    radio2 = (
        ui.radio([ui.option('A', 1), ui.option('B', 2), ui.option('C', 3)])
        .props('inline')
        .bind_value(radio1, 'value')
    )


@doc.demo('Inject arbitrary content', '''
    Thanks to the [`ui.teleport` element](teleport), you can use arbitrary content for the radio options.
''')
def arbitrary_content():
    options = ['Star', 'Thump Up', 'Heart']
    radio = ui.radio({x: '' for x in options}, value='Star').props('inline')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(1) .q-radio__label'):
        ui.icon('star', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(2) .q-radio__label'):
        ui.icon('thumb_up', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(3) .q-radio__label'):
        ui.icon('favorite', size='md')
    ui.label().bind_text_from(radio, 'value')


doc.reference(Radio)
