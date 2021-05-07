import nice_gui as ui
from icecream import ic

app = ui.app()

ui.Label('Hello Nice GUI!')

ui.Button('BUTTON', on_click=lambda _: ui.Label('Nice!'))
