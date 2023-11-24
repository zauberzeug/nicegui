from nicegui import ui

from ..model import UiElementDocumentation


class ImageDocumentation(UiElementDocumentation, element=ui.image):

    def main_demo(self) -> None:
        ui.image('https://picsum.photos/id/377/640/360')

    def more(self) -> None:
        ui.add_body_html(
            '<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

        @self.demo('Local files', '''
            You can use local images as well by passing a path to the image file.
        ''')
        def local():
            ui.image('website/static/logo.png').classes('w-16')

        @self.demo('Base64 string', '''
            You can also use a Base64 string as image source.
        ''')
        def base64():
            base64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
            ui.image(base64).classes('w-2 h-2 m-auto')

        @self.demo('PIL image', '''
            You can also use a PIL image as image source.
        ''')
        def pil():
            import numpy as np
            from PIL import Image

            image = Image.fromarray(np.random.randint(0, 255, (100, 100), dtype=np.uint8))
            ui.image(image).classes('w-32')

        @self.demo('Lottie files', '''
            You can also use [Lottie files](https://lottiefiles.com/) with animations.
        ''')
        def lottie():
            # ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

            src = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'
            ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-full')

        @self.demo('Image link', '''
            Images can link to another page by wrapping them in a [ui.link](https://nicegui.io/documentation/link).
        ''')
        def link():
            with ui.link(target='https://github.com/zauberzeug/nicegui'):
                ui.image('https://picsum.photos/id/41/640/360').classes('w-64')

        @self.demo('Force reload', '''
            You can force an image to reload by calling the `force_reload` method.
            It will append a timestamp to the image URL, which will make the browser reload the image.
        ''')
        def force_reload():
            img = ui.image('https://picsum.photos/640/360').classes('w-64')

            ui.button('Force reload', on_click=img.force_reload)
