from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    ui.icon('thumb_up').classes('text-5xl')


def more() -> None:
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')

    @text_demo('Eva icons', '''
        You can use [Eva icons](https://akveo.github.io/eva-icons/#/) in your app.
    ''')
    async def eva_icons():
        # ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
        ui.element('i').classes('eva eva-github').classes('text-5xl')
