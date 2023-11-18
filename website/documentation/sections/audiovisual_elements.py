from nicegui import ui

from ..tools import load_demo, text_demo

name = 'audiovisual_elements'
title = 'Audiovisual Elements'


def intro() -> None:
    ...


def content() -> None:
    load_demo(ui.image)

    @text_demo('Captions and Overlays', '''
        By nesting elements inside a `ui.image` you can create augmentations.

        Use [Quasar classes](https://quasar.dev/vue-components/img) for positioning and styling captions.
        To overlay an SVG, make the `viewBox` exactly the size of the image and provide `100%` width/height to match the actual rendered size.
    ''')
    def captions_and_overlays_demo():
        with ui.image('https://picsum.photos/id/29/640/360'):
            ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

        with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
            ui.html('''
                <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="20" />
                </svg>
            ''').classes('bg-transparent')

    load_demo(ui.interactive_image)
    load_demo(ui.audio)
    load_demo(ui.video)
    load_demo(ui.icon)
    load_demo(ui.avatar)

    @text_demo('SVG',
               'You can add Scalable Vector Graphics using the `ui.html` element.')
    def svg_demo():
        content = '''
            <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
            <circle cx="80" cy="85" r="8" />
            <circle cx="120" cy="85" r="8" />
            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
            </svg>'''
        ui.html(content)
