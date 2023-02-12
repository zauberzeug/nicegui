#!/usr/bin/env python3
from nicegui import ButtonLayout, ui

ui.icon('star').layout.color('yellow', '8').size.medium().align.center()

shared_row = ui.layout('horizontal').size(width='full').background('secondary')

with shared_row.copy().padding.y_axis.small().align.children(main_axis='center'):
    for i in range(5):
        with ui.card():
            ui.label(str(i))

button_layout = ButtonLayout().rounded().background('teal', '9')
hover = ui.layout().text.gray(0.6)

with shared_row.copy().size(height='20').background('grey', '4').align.children(main_axis='evenly', cross_axis='center'):
    ui.button('12').layout.square().size(width='12').add(button_layout)
    ui.button('64').layout.size(width='64', height='2/3').add(button_layout)
    ui.button('1/6').layout.size(width='1/6').add(button_layout).on_hover(hover)

with shared_row.copy().gap.none():
    ui.image('https://picsum.photos/id/29/640/360').layout.size(width='1/2')
    ui.image('https://picsum.photos/id/565/640/360').layout.size(width='1/2')

with ui.layout('horizontal').size(width='full').align.children(cross_axis='center'):
    progress = ui.element('div').layout.size(width='1/2', height='6')\
        .opacity(0.3).background('primary').element
    ui.label('transparency')
    ui.toggle([0.3, 0.5, 1.0], value=0.5, on_change=progress.update).\
        bind_value_to(progress.layout.bindables, 'opacity').layout.margin.left.auto()

with ui.layout('horizontal', subdivision=2).size(width='full').gap.large():
    with ui.layout('horizontal', subdivision=2).background('white'):
        [ui.element().layout.background('grey', str(shade)).size(height='6') for shade in range(2, 8)]
        ui.element().classes('col-span-2').layout.background('grey', '9').size('full', '12')
    with ui.layout('vertical', subdivision=2).background('white'):
        [ui.element().layout.background('grey', str(shade)).size(height='full') for shade in range(2, 8)]
        ui.element().classes('row-span-2').layout.background('grey', '9').size('full', 'full')

ui.run()
