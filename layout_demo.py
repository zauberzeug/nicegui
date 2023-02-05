#!/usr/bin/env python3
from nicegui import ButtonLayout, Layout, ui

ui.markdown('''### Features
- auto completion + documentation for common layout and styling aspects through builder pattern
- nesting layout aspects of arbitrary depth: `align.main_axis.evenly()`, thereby reducing number of options to search through
- error reports for invalid layout aspects (e.g. `margin.top.auto()` is not possible with css)
- the Layout of an existing element can be modify by accessing its layout property
- Layouts can be created independently because they are just objects
- Layouts can be used as contexts to create generic groups, rows, columns: `with ui.layout().row()`
- specialized Layouts can provide additional styling (e.g. `ButtonLayout` to configure shape etc.)
- a Layout can be applied to (multiple) elements via `add`
- a Layout is copied by invoking the object (just a shortcut for layout factory functions)
''')

ui.icon('star').layout.color.yellow(0.8).size.medium().align.center()

shared_row = Layout().size(width='full').background.secondary().row()

with shared_row().padding.y_axis.small().align.main_axis.center():
    for i in range(5):
        with ui.card():
            ui.label(str(i))

button_layout = ButtonLayout().rounded().background.teal(0.9)
hover = Layout().text.gray(0.6)

with shared_row().size(height='20').background.grey(0.4).align.main_axis.evenly().align.cross_axis.center():
    ui.button('12').layout.square().size(width='12').add(button_layout)
    ui.button('64').layout.size(width='64', height='2/3').add(button_layout)
    ui.button('1/6').layout.size(width='1/6').add(button_layout).on_hover(hover)

with shared_row().gap.none():
    ui.image('https://picsum.photos/id/29/640/360').layout.size(width='1/2')
    ui.image('https://picsum.photos/id/565/640/360').layout.size(width='1/2')

with ui.layout().row().size(width='full').align.cross_axis.center():
    progress = ui.element('div').layout.size(width='1/2', height='6')\
        .opacity(0.3).background.primary().element
    ui.label('transparency')
    ui.toggle([0.3, 0.5, 1.0], value=0.5, on_change=progress.update).\
        bind_value_to(progress.layout.bindables, 'opacity').layout.margin.left.auto()


ui.run()
