from nicegui import ui

from . import doc


@doc.demo(ui.slide_item)
def main_demo() -> None:
    with ui.list().props('bordered separator'):
        with ui.slide_item('Slide me left or right') as slide_item_1:
            slide_item_1.left('Left', color='green')
            slide_item_1.right('Right', color='red')
        with ui.slide_item('Slide me up or down') as slide_item_2:
            slide_item_2.top('Top', color='blue')
            slide_item_2.bottom('Bottom', color='purple')


@doc.demo('More complex layout', '''
    You can fill the slide item and its action slots with custom UI elements.
''')
def complex_demo():
    with ui.list().props('bordered'):
        with ui.slide_item() as slide_item:
            with ui.item():
                with ui.item_section().props('avatar'):
                    ui.icon('person')
                with ui.item_section():
                    ui.item_label('Alice A. Anderson')
                    ui.item_label('CEO').props('caption')
            with slide_item.left(on_slide=lambda: ui.notify('Calling...')):
                with ui.item(on_click=slide_item.reset):
                    with ui.item_section().props('avatar'):
                        ui.icon('phone')
                    ui.item_section('Call')
            with slide_item.right(on_slide=lambda: ui.notify('Texting...')):
                with ui.item(on_click=slide_item.reset):
                    ui.item_section('Text')
                    with ui.item_section().props('avatar'):
                        ui.icon('message')


@doc.demo('Slide handlers', '''
    An event handler can be triggered when a specific side is selected.
''')
def slide_callbacks():
    with ui.list().props('bordered'):
        with ui.slide_item('Slide me', on_slide=lambda e: ui.notify(f'Slide: {e.side}')) as slide_item:
            slide_item.left('A', on_slide=lambda e: ui.notify(f'A ({e.side})'))
            slide_item.right('B', on_slide=lambda e: ui.notify(f'B ({e.side})'))


@doc.demo('Resetting the slide item', '''
    After a slide action has occurred, the slide item can be reset back to its initial state using the ``reset`` method.
''')
def slide_reset():
    with ui.list().props('bordered'):
        with ui.slide_item() as slide_item:
            ui.item('Slide me')
            with slide_item.left(color='blue'):
                ui.item('Left')
            with slide_item.right(color='purple'):
                ui.item('Right')

    ui.button('Reset', on_click=slide_item.reset)


doc.reference(ui.slide_item)
