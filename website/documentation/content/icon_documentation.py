from nicegui import ui

from . import doc


@doc.demo(ui.icon)
def main_demo() -> None:
    ui.icon('thumb_up', color='primary').classes('text-5xl')


@doc.demo('Material icons and symbols', '''
    You can use different sets of Material icons and symbols.
    The [Quasar documentation](https://quasar.dev/vue-components/icon#webfont-usage)
    gives an overview of all available icon sets and their name prefix:
    
    * None for [filled icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Filled)
    * "o\_" for [outline icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Outlined)
    * "r\_" for [round icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Rounded)
    * "s\_" for [sharp icons](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Sharp)
    * "sym\_o\_" for [outline symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined)
    * "sym\_r\_" for [round symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)
    * "sym\_s\_" for [sharp symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Sharp)
''')
def material_icons():
    with ui.row().classes('text-4xl'):
        ui.icon('home')
        ui.icon('o_home')
        ui.icon('r_home')
        ui.icon('sym_o_home')
        ui.icon('sym_r_home')


@doc.demo('Eva icons', '''
    You can use [Eva icons](https://akveo.github.io/eva-icons/) in your app.
''', lazy=False)
def eva_icons():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet"/>')

    ui.element('i').classes('eva eva-github').classes('text-5xl')


@doc.demo('Other icon sets', '''
    You can use the same approach for adding other icon sets to your app. 
    As a rule of thumb, you reference the corresponding CSS, and it in turn references font files.
    We will show how to include [Themify icons](https://themify.me/themify-icons):
''', lazy=False)
def other_icons():
    ui.add_head_html('<link rel="stylesheet" href="https://cdn.jsdelivr.net/themify-icons/0.1.2/css/themify-icons.css"/>')
    
    ui.icon('ti-car')


@doc.demo('Lottie files', '''
    You can also use [Lottie files](https://lottiefiles.com/) with animations.
''', lazy=False)
def lottie():
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    src = 'https://assets5.lottiefiles.com/packages/lf20_MKCnqtNQvg.json'
    ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-24')


doc.reference(ui.icon)
