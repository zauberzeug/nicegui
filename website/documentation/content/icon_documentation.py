from nicegui import ui

from . import doc


@doc.demo(ui.icon)
def main_demo() -> None:
    ui.icon('thumb_up', color='primary').classes('text-5xl')


@doc.demo('Eva icons', '''
    You can use [Eva icons](https://akveo.github.io/eva-icons/) in your app.
''', lazy=False)
def eva_icons():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')

    ui.element('i').classes('eva eva-github').classes('text-5xl')


@doc.demo('Lottie files', '''
    You can also use [Lottie files](https://lottiefiles.com/) with animations.
''', lazy=False)
def lottie():
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    src = 'https://assets5.lottiefiles.com/packages/lf20_MKCnqtNQvg.json'
    ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-24')


doc.reference(ui.icon)
