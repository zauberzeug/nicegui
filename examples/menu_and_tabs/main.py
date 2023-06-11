from nicegui import ui

with ui.header().classes(replace="row items-center") as header:
    ui.button(on_click=lambda: left_drawer.toggle()).props("flat color=white icon=menu")
    with ui.tabs() as tabs:
        ui.tab("A")
        ui.tab("B")
        ui.tab("C")

with ui.footer(value=False) as footer:
    ui.label("Footer")

with ui.left_drawer().classes("bg-blue-100") as left_drawer:
    ui.label("Side menu")

with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle).props("fab icon=contact_support")

with ui.tab_panels(tabs, value="Home").classes("w-full"):
    with ui.tab_panel("A"):
        ui.label("Content of A")
    with ui.tab_panel("B"):
        ui.label("Content of B")
    with ui.tab_panel("C"):
        ui.label("Content of C")

ui.run()
