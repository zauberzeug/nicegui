from nicegui import ui

from . import doc


@doc.demo(ui.slide_item)
def main_demo() -> None:
    with ui.list().props('separator'):
        with ui.slide_item() as slide_item_one:
            ui.item('Slide me Left or Right')
            with slide_item_one.slide('left', color='green'):
                ui.label('Left')
            with slide_item_one.slide('right', color='red'):
                ui.label('Right')
        with ui.slide_item() as slide_item_two:
            ui.item('Slide me Up or Down')
            with slide_item_two.slide('top', color='blue'):
                ui.label('Top')
            with slide_item_two.slide('bottom', color='purple'):
                ui.label('Bottom')


@doc.demo('Change and Slide Callbacks', '''
    A callback function can be triggered when the slide changes and when a specific side is selected.
''')
def slide_callbacks():
    with ui.list().props('separator'):
        with ui.slide_item(on_change=lambda: ui.notify('Slide changed')) as slide_item:
            ui.item('Slide me Left or Right')
            with slide_item.slide('left', on_slide=lambda s: ui.notify(f'Slide {s.args} triggered')):
                ui.icon('arrow_back')
            with slide_item.slide('right', on_slide=lambda s: ui.notify(f'Slide {s.args} triggered')):
                ui.icon('arrow_forward')


@doc.demo('Resetting the Slide Item', '''
    Once a slide action has occurred, the slide item can be reset back to initial state.
''')
def slide_reset():
    with ui.list().props('separator'):
        with ui.slide_item() as slide_item:
            ui.item('Slide me Up or Down')
            with slide_item.slide('top', color='blue'):
                ui.label('Top')
            with slide_item.slide('bottom', color='purple'):
                ui.label('Bottom')

    ui.button('Reset Slide Item', on_click=slide_item.reset)
