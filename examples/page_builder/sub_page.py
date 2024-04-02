from nicegui import ui


@ui.page('/sub_page')
def sub_page():
    ui.label('Sub Page').classes('text-2xl')
