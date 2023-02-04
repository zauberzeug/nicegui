#!/usr/bin/env python3
from nicegui import ButtonLooks, Looks, ui

shared = Looks().width.full().background.secondary()

with ui.row().looks.add(shared).padding.y_axis.small().align.main_axis.center().element:
    for i in range(5):
        with ui.card():
            ui.label(str(i))

button_looks = ButtonLooks().rounded().background.teal(0.9)
hover = Looks().text.gray(0.6)

with ui.row().looks.add(shared).height.fixed.twenty().background.grey(0.4).align.main_axis.evenly().align.cross_axis.center().element:
    ui.button('12').looks.square().width.fixed.twelve().add(button_looks)
    ui.button('64').looks.width.fixed.sixty_four().add(button_looks).height.fractional.two_thirds()
    ui.button('1/6').looks.width.fractional.one_sixth().add(button_looks).on_hover(hover)

with ui.row().looks.add(shared).gap.none().element:
    ui.image('https://picsum.photos/id/29/640/360').looks.width.fractional.one_half()
    ui.image('https://picsum.photos/id/565/640/360').looks.width.fractional.one_half()

ui.run()
