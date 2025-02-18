from nicegui import ui

from . import doc


@doc.demo(ui.colors)
def main_demo() -> None:
    # ui.button('Default', on_click=lambda: ui.colors())
    # ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))
    # END OF DEMO
    b1 = ui.button('Default', on_click=lambda: [b.classes(replace='!bg-primary') for b in [b1, b2]])
    b2 = ui.button('Gray', on_click=lambda: [b.classes(replace='!bg-[#555]') for b in [b1, b2]])


@doc.demo('Custom colors', '''
    You can add custom color definitions for branding.
    In this case, `ui.colors` must be called before the custom color is ever used.

    *Added in version 2.2.0*
''')
def custom_color_demo() -> None:
    from random import randint

    ui.colors(brand='#424242')
    ui.label('This is your custom brand color').classes('text-brand')
    ui.button('Randomize', color='brand',
              on_click=lambda: ui.colors(brand=f'#{randint(0, 0xffffff):06x}'))


doc.reference(ui.colors)
