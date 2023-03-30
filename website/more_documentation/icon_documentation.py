from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    ui.icon('thumb_up').classes('text-5xl')


def more() -> None:
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    @text_demo('Eva icons', '''
        You can use [Eva icons](https://akveo.github.io/eva-icons/#/) in your app.
    ''')
    async def eva_icons():
        # ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
        ui.element('i').classes('eva eva-github').classes('text-5xl')

    @text_demo('Lottie', '''
        You can also use [Lottie files](https://lottiefiles.com/) with animations.
    ''')
    async def lottie():
        # ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

        ui.html('''
        <lottie-player src="https://assets5.lottiefiles.com/packages/lf20_MKCnqtNQvg.json"  
        background="transparent"  speed="1" style="width: 80px; height: 80px;" loop autoplay></lottie-player>
        ''')
