#!/usr/bin/env python3
from nicegui import ButtonLayout, Layout, ui

ui.markdown('''### Features
- auto completion + documentation for simple to understand layout and styling aspects
- using the builder pattern in combination with string literals
- logically grouping of layout aspects (e.g. `align.center` and `align.children` are fundamentally different in css but presented together)
- the Layout of an existing element can be modify by accessing its layout property
- Layouts can also be created independently because they are just objects
- element.props and element.classes take precedence over element.layout definitions to allow customizations
- Layouts can be used as contexts to create generic groups, rows, columns: `with ui.layout().row()`
- specialized Layouts provide additional styling (e.g. `ButtonLayout` to configure shape etc.)
- a Layout can be applied to (multiple) elements via `add`
- a Layout can duplicated by calling `.copy()`
- error reports for invalid layout aspects (e.g. `margin.top.auto()` is not possible with css)

### ToDos / Ideas
- Layout.row() and Layout.column() should use a GroupLayout which provides arrangement of children (e.g. gap, align.children, ...)
- Some mechanism to allow using Quasar columns
- Some mechanism to allow Grid and Masonry Layouts
''')

ui.icon('star').layout.color('yellow', '8').size.medium().align.center()

shared_row = Layout().size(width='full').background('secondary').row()

with shared_row.copy().padding.y_axis.small().align.children(main_axis='center'):
    for i in range(5):
        with ui.card():
            ui.label(str(i))

button_layout = ButtonLayout().rounded().background('teal', '9')
hover = Layout().text.gray(0.6)

with shared_row.copy().size(height='20').background('grey', '4').align.children(main_axis='evenly', cross_axis='center'):
    ui.button('12').layout.square().size(width='12').add(button_layout)
    ui.button('64').layout.size(width='64', height='2/3').add(button_layout)
    ui.button('1/6').layout.size(width='1/6').add(button_layout).on_hover(hover)

with shared_row.copy().gap.none():
    ui.image('https://picsum.photos/id/29/640/360').layout.size(width='1/2')
    ui.image('https://picsum.photos/id/565/640/360').layout.size(width='1/2')

with ui.layout().row().size(width='full').align.children(cross_axis='center'):
    progress = ui.element('div').layout.size(width='1/2', height='6')\
        .opacity(0.3).background('primary').element
    ui.label('transparency')
    ui.toggle([0.3, 0.5, 1.0], value=0.5, on_change=progress.update).\
        bind_value_to(progress.layout.bindables, 'opacity').layout.margin.left.auto()


ui.run()
