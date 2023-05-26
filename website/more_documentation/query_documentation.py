from nicegui import globals, ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    def set_background(color: str) -> None:
        ui.query('body').style(f'background-color: {color}')

    # ui.button('Blue', on_click=lambda: set_background('#ddeeff'))
    # ui.button('Orange', on_click=lambda: set_background('#ffeedd'))
    # END OF DEMO
    ui.button('Blue', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ddeeff'))
    ui.button('Orange', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ffeedd'))


def more() -> None:
    @text_demo('Set background gradient', '''
        It's easy to set a background gradient, image or similar. 
        See [w3schools.com](https://www.w3schools.com/cssref/pr_background-image.php) for more information about setting background with CSS.
    ''')
    def background_image():
        # ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')
        # END OF DEMO
        globals.get_slot_stack()[-1].parent.classes('bg-gradient-to-t from-blue-400 to-blue-100')
