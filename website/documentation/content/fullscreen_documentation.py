from nicegui import ui

from . import doc


@doc.demo(ui.fullscreen)
def main_demo() -> None:
    fullscreen = ui.fullscreen()

    ui.button('Enter Fullscreen', on_click=fullscreen.enter)
    ui.button('Exit Fullscreen', on_click=fullscreen.exit)
    ui.button('Toggle Fullscreen', on_click=fullscreen.toggle)


@doc.demo('Requiring long-press to exit', '''
    You can require users to long-press the escape key to exit fullscreen mode.
    This is useful to prevent accidental exits, for example when working on forms or editing data.

    Note that this feature only works in some browsers like Google Chrome or Microsoft Edge.
''')
def long_press_demo():
    fullscreen = ui.fullscreen()
    ui.switch('Require escape hold').bind_value_to(fullscreen, 'require_escape_hold')
    ui.button('Toggle Fullscreen', on_click=fullscreen.toggle)


@doc.demo('Tracking fullscreen state', '''
    You can track when the fullscreen state changes.

    Note that due to security reasons, fullscreen mode can only be entered from a previous user interaction
    such as a button click.
''')
def state_demo():
    fullscreen = ui.fullscreen(
        on_state_change=lambda e: ui.notify('Enter' if e.value else 'Exit')
    )
    ui.button('Toggle Fullscreen', on_click=fullscreen.toggle)
    ui.label().bind_text_from(fullscreen, 'state',
                              lambda state: 'Fullscreen' if state else '')


doc.reference(ui.fullscreen)
