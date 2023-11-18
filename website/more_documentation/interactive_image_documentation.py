from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    from nicegui.events import MouseEventArguments

    def mouse_handler(e: MouseEventArguments):
        color = 'SkyBlue' if e.type == 'mousedown' else 'SteelBlue'
        ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
        ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

    src = 'https://picsum.photos/id/565/640/360'
    ii = ui.interactive_image(src, on_mouse=mouse_handler, events=['mousedown', 'mouseup'], cross=True)


def more() -> None:
    @text_demo('Nesting elements', '''
        You can nest elements inside an interactive image.
        Use Tailwind classes like "absolute top-0 left-0" to position the label absolutely with respect to the image.
        Of course this can be done with plain CSS as well.
    ''')
    def nesting_elements():
        with ui.interactive_image('https://picsum.photos/id/147/640/360'):
            ui.button(on_click=lambda: ui.notify('thumbs up'), icon='thumb_up') \
                .props('flat fab color=white') \
                .classes('absolute bottom-0 left-0 m-2')

    @text_demo('Force reload', '''
        You can force an image to reload by calling the `force_reload` method.
        It will append a timestamp to the image URL, which will make the browser reload the image.
    ''')
    def force_reload():
        img = ui.interactive_image('https://picsum.photos/640/360').classes('w-64')

        ui.button('Force reload', on_click=img.force_reload)
