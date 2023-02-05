#!/usr/bin/env python3
from nicegui import ButtonLayout, Layout, ui

shared = Layout().width.full().background.secondary()

with ui.row().layout.add(shared).padding.y_axis.small().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

button_layout = ButtonLayout().rounded().background.teal(0.9)
hover = Layout().text.gray(0.6)

with ui.row().layout.add(shared).height.fixed.twenty().background.grey(0.4).align.main_axis.evenly().align.cross_axis.center().element:
    ui.button('12').layout.square().width.fixed.twelve().add(button_layout)
    ui.button('64').layout.width.fixed.sixty_four().add(button_layout).height.fractional.two_thirds()
    ui.button('1/6').layout.width.fractional.one_sixth().add(button_layout).on_hover(hover)

with ui.row().layout.add(shared).gap.none().element:
    ui.image('https://picsum.photos/id/29/640/360').layout.width.fractional.one_half()
    ui.image('https://picsum.photos/id/565/640/360').layout.width.fractional.one_half()

with ui.row().layout.width.full().align.cross_axis.center().element:
    progress = ui.element('div').layout.width.fractional.one_half().height.fixed.six()\
        .opacity(0.3).background.primary().element
    ui.label('transparency')
    ui.toggle([0.3, 0.5, 1.0], value=0.5, on_change=progress.update).\
        bind_value_to(progress.layout.bindables, 'opacity').layout.margin.left.auto()

ui.run()
