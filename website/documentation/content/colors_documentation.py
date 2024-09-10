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
    You can add custom color definitions for branding. In this case, `ui.colors` must be called before the
    custom color is ever used.
''')
def custom_color_demo() -> None:
    import random

    def random_color():
        return f'#{random.randint(0, 0xffffff):06x}'

    ui.colors(my_custom_color=random_color())
    ui.button(
        'Random color',
        color='my-custom-color',
        on_click=lambda: ui.colors(my_custom_color=random_color())
    )


doc.reference(ui.colors)
