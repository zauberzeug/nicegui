#!/usr/bin/env python3
from backgrounds import Backgrounds
from sizing import Sizing
from typography import Typography

from nicegui import ui

s_title = Typography() \
    .text_color('text-teal-600') \
    .font_size('text-5xl') \
    .text_transform('uppercase') \
    .text_align('text-center')

s_full_width = Sizing().width('w-full')

with ui.left_drawer() as sidebar:
    page_title = ui.label('Title')

with ui.card() as main:
    ui.label('Lorem Ipsum')
    ui.separator()
    with ui.row() as btns:
        Typography(ui.label('label 1')).text_color('text-amber-700').element.tooltip('label 1')
        Typography(ui.label('label 2')).text_color('text-orange-900').element.tooltip('label 2')

s_title.apply(page_title)
s_full_width.apply(main)
s_full_width.apply(btns)

Backgrounds(main).background_color('bg-lime-200')
Backgrounds(sidebar).background_color('bg-orange-200')

ui.run()
