from nicegui import ui


def main_demo() -> None:
    async def alert():
        await ui.run_javascript('alert("Hello!")', respond=False)

    async def get_date():
        time = await ui.run_javascript('Date()')
        ui.notify(f'Browser time: {time}')

    async def access_elements():
        await ui.run_javascript(f'getElement({label.id}).innerText += " Hello!"')

    ui.button('fire and forget', on_click=alert)
    ui.button('receive result', on_click=get_date)
    ui.button('access elements', on_click=access_elements)
    label = ui.label()
