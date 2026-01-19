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


@doc.demo('App-wide colors', '''
    You can set app-wide colors using `app.colors()`.

    The API is same as the initializer of `ui.colors()`,
    but the colors will be applied to all pages unless overridden by `ui.colors()` on a specific page.

    *Added in version 3.6.0*
''')
def app_colors_demo() -> None:
    # from nicegui import app
    # app.colors(primary='#B0C4DE', brand='#FF6347')

    # @ui.page('/')
    def page():
        # ui.button('App-Wide Primary Color')
        # ui.button('App-Wide Brand Color', color='brand')
        ui.button('App-Wide Primary Color', color='#B0C4DE')  # HIDE
        ui.button('App-Wide Brand Color', color='#FF6347')  # HIDE
    page()  # HIDE


doc.reference(ui.colors)
