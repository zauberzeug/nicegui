from nice_gui import ui
from datetime import datetime
from icecream import ic

ui.label('Hello, Nice GUI!')

with ui.column() as c:
    c.button('BUTTON', on_click=lambda _: c.label('Nice!'))

time = ui.label('Time: ')


def update_time():
    time.text = f'Time: {datetime.now().strftime("%H:%M:%S")}'


ui.timer(1, update_time)
