#!/usr/bin/env python3
from number_checker import NumberChecker

from nicegui import ui


@ui.page('/')
def page():
    number_checker = NumberChecker()
    number = ui.number(value=42.0)

    async def check():
        even = await number_checker.is_even(number.value)
        ui.notify(f'{number.value} is {"even" if even else "odd"}')

    ui.button('Check', on_click=check)


ui.run()
