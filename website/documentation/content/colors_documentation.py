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

    A custom color name works wherever Quasar accepts a color name,
    e.g. the `color` parameter and the `color` and `text-color` props,
    as well as the classes `text-<name>` and `bg-<name>`.
    Underscores in the name become dashes, e.g. `warn_soft` is used as `warn-soft`.
    These classes are marked `!important`, so they override Quasar's default colors
    and there is no need for inline styles.

    *Added in version 2.2.0*
''')
def custom_color_demo() -> None:
    from random import randint

    ui.colors(brand='#424242')
    ui.label('This is your custom brand color').classes('text-brand')
    ui.button('Randomize', color='brand',
              on_click=lambda: ui.colors(brand=f'#{randint(0, 0xffffff):06x}'))
    ui.button('Outline', icon='palette').props('outline text-color=brand')


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
        # ui.button('App-wide primary color')
        # ui.button('App-wide brand color', color='brand')
        ui.button('App-wide primary color', color='#B0C4DE').classes('text-white')  # HIDE
        ui.button('App-wide brand color', color='#FF6347').classes('text-white')  # HIDE
    page()  # HIDE


doc.reference(ui.colors)
