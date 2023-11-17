from nicegui import ui


def main_demo() -> None:
    from nicegui import app

    # ui.button('shutdown', on_click=app.shutdown)
    #
    # ui.run(reload=False)
    # END OF DEMO
    ui.button('shutdown', on_click=lambda: ui.notify(
        'Nah. We do not actually shutdown the documentation server. Try it in your own app!'))
