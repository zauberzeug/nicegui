from nicegui import context, ui

from . import doc


@doc.demo(ui.query)
def main_demo() -> None:
    def set_background(color: str) -> None:
        ui.query('body').style(f'background-color: {color}')

    # ui.button('Blue', on_click=lambda: set_background('#ddeeff'))
    # ui.button('Orange', on_click=lambda: set_background('#ffeedd'))
    # END OF DEMO
    ui.button('Blue', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ddeeff'))
    ui.button('Orange', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ffeedd'))


@doc.demo('Set background gradient', '''
    It's easy to set a background gradient, image or similar.
    See [w3schools.com](https://www.w3schools.com/cssref/pr_background-image.php) for more information about setting background with CSS.
''')
def background_image():
    # ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')
    # END OF DEMO
    context.get_slot_stack()[-1].parent.classes('bg-gradient-to-t from-blue-400 to-blue-100')


@doc.demo('Modify default page padding', '''
    By default, NiceGUI provides a built-in padding around the content of the page.
    You can modify it using the class selector `.nicegui-content`.
''')
def remove_padding():
    # ui.query('.nicegui-content').classes('p-0')
    context.get_slot_stack()[-1].parent.classes(remove='p-4')  # HIDE
    # with ui.column().classes('h-screen w-full bg-gray-400 justify-between'):
    with ui.column().classes('h-full w-full bg-gray-400 justify-between'):  # HIDE
        ui.label('top left')
        ui.label('bottom right').classes('self-end')


doc.reference(ui.query)
