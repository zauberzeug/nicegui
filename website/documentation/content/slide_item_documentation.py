from nicegui import ui

from . import doc


@doc.demo(ui.slide_item)
def main_demo() -> None:
    with ui.list().props('dense separator'):
        with ui.slide_item():
            with ui.item_section().classes('h-20'):
                ui.item_label('Slide me Left or Right')
            with ui.left_slide(color='green'):
                ui.item_label('Left')
            with ui.right_slide(color='red'):
                ui.item_label('Right')
        with ui.slide_item():
            with ui.item_section().classes('h-20'):
                ui.item_label('Slide me Up or Down')
            with ui.top_slide(color='blue'):
                ui.item_label('Top')
            with ui.bottom_slide(color='purple'):
                ui.item_label('Bottom')


@doc.demo('Change and Slide Callbacks', '''
    A callback function can be triggered when the slide changes and when a specific side is selected.
''')
def slide_callbacks():
    with ui.list().props('dense separator'):
        with ui.slide_item(on_change=lambda: ui.notify('Slide changed')):
            with ui.item_section().classes('h-20'):
                ui.item_label('Slide me Left or Right')
            with ui.left_slide(on_slide=lambda s: ui.notify(f'Slide {s.args} triggered')):
                ui.icon('arrow_back')
            with ui.right_slide(on_slide=lambda s: ui.notify(f'Slide {s.args} triggered')):
                ui.icon('arrow_forward')


@doc.demo('Resetting the Slide Item', '''
    Once a Slide action has occured the Slide Item can be reset back to initial state.
''')
def slide_reset():
    with ui.list().props('dense separator'):
        with ui.slide_item() as slide_item:
            with ui.item_section().classes('h-20'):
                ui.item_label('Slide me Up or Down')
            with ui.top_slide(color='blue'):
                ui.item_label('Top')
            with ui.bottom_slide(color='purple'):
                ui.item_label('Bottom')

    ui.button('Reset Slide Item', on_click=lambda: slide_item.reset())


doc.reference(ui.left_slide, title='Reference for ui.left_slide')
doc.reference(ui.right_slide, title='Reference for ui.left_slide')
doc.reference(ui.top_slide, title='Reference for ui.top_slide')
doc.reference(ui.bottom_slide, title='Reference for ui.bottom_slide')
