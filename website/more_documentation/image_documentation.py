from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.image('https://picsum.photos/id/377/640/360')


def more() -> None:
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    @text_demo('Local files', '''
        You can use local images as well by passing a path to the image file.
    ''')
    def local():
        ui.image('website/static/logo.png').classes('w-16')

    @text_demo('Lottie files', '''
        You can also use [Lottie files](https://lottiefiles.com/) with animations.
    ''')
    def lottie():
        # ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

        src = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'
        ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-full')
