#!/usr/bin/env python3
from nicegui import app, ui

app.add_static_files('/images', '.')

img_src = '/images/PpIqU.png'
mask_src = '/images/OfwWp.png'

with ui.row().classes('w-full flex items-center'):
    ui.image(img_src).style('width: 25%')
    ui.label('+').style('font-size: 18em')
    ui.image(mask_src).style('width: 25%')
    ui.label('=').style('font-size: 18em')
    image = ui.interactive_image(img_src).style('width: 25%')
    image.content = f'''
        <image xlink:href="{mask_src}" width="100%" height="100%" x="0" y="0" filter="url(#mask)" />
        <filter id="mask">
            <feComponentTransfer>
                <feFuncR type="linear" slope="40" />
                <feFuncG type="linear" slope="40" />
                <feFuncB type="linear" slope="40" />
                <feFuncR type="linear" slope="1000" />
            </feComponentTransfer>
            <feColorMatrix type="matrix" values="1 0 0 0 0   0 1 0 0 0   0 0 1 0 0  3 -1 -1 0 0" />
        </filter>
    '''
ui.markdown(
    'Images where discovered through <https://stackoverflow.com/a/57579290/364388>. '
    'SVG filters where used to colorize the mask. You may want to check out <https://webplatform.github.io/docs/svg/tutorials/smarter_svg_filters/>.'
).classes('mt-4')

ui.run()
