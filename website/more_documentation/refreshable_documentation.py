from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    import random

    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label(', '.join(str(n) for n in sorted(numbers)))

    def add_number() -> None:
        numbers.append(random.randint(0, 100))
        number_ui.refresh()

    number_ui()
    ui.button('Add random number', on_click=add_number)


def more() -> None:
    @text_demo('Refreshable UI with parameters', '''
        Here is a demo of how to use the refreshable decorator to create a UI that can be refreshed with different parameters.
    ''')
    def refreshable_with_parameters():
        from datetime import datetime

        import pytz

        @ui.refreshable
        def clock_ui(timezone: str):
            ui.label(f'Current time in {timezone}:')
            ui.label(datetime.now(tz=pytz.timezone(timezone)).strftime('%H:%M:%S'))

        clock_ui('Europe/Berlin')
        ui.button('Refresh', on_click=clock_ui.refresh)
        ui.button('Refresh for New York', on_click=lambda: clock_ui.refresh('America/New_York'))
        ui.button('Refresh for Tokyo', on_click=lambda: clock_ui.refresh('Asia/Tokyo'))

    @text_demo('Refreshable UI for input validation', '''
        Here is a demo of how to use the refreshable decorator to give feedback about the validity of user input.
    ''')
    def input_validation():
        import re

        pwd = ui.input('Password', password=True, on_change=lambda: show_info.refresh())

        rules = {
            'Lowercase letter': lambda s: re.search(r'[a-z]', s),
            'Uppercase letter': lambda s: re.search(r'[A-Z]', s),
            'Digit': lambda s: re.search(r'\d', s),
            'Special character': lambda s: re.search(r"[!@#$%^&*(),.?':{}|<>]", s),
            'min. 8 characters': lambda s: len(s) >= 8,
        }

        @ui.refreshable
        def show_info():
            for rule, check in rules.items():
                with ui.row().classes('items-center gap-2'):
                    if check(pwd.value or ''):
                        ui.icon('done', color='green')
                        ui.label(rule).classes('text-xs text-green strike-through')
                    else:
                        ui.icon('radio_button_unchecked', color='red')
                        ui.label(rule).classes('text-xs text-red')

        show_info()
