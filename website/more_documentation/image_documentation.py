from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.image('https://picsum.photos/id/377/640/360')


def more() -> None:
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    @text_demo('Base64 string', '''
        You can also use a Base64 string as image source.
    ''')
    def base64():
        base64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
        ui.image(base64).classes('w-2 h-2 m-auto')

    @text_demo('Lottie files', '''
        You can also use [Lottie files](https://lottiefiles.com/) with animations.
    ''')
    def lottie():
        # ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

        src = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'
        ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-full')
