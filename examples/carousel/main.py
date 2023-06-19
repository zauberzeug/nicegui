from nicegui import ui

image_urls = [
    'https://picsum.photos/300/300?1',
    'https://picsum.photos/300/300?2',
    'https://picsum.photos/300/300?3',
]

tabs = {}

def switch_tab(value):
    tabs['panels'].value = value

# Create tab_bar object, but don't render it in a UI component
tab_bar = ui.tabs()
# tabs['A'] = tab_bar.tab('A')
# tabs['B'] = tab_bar.tab('B')
# tabs['C'] = tab_bar.tab('C')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tab_bar, value='A').classes('w-full') as panels:
    tabs['panels'] = panels

    with ui.tab_panel('A') as tabA:
        ui.label('Content of A').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[0]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_back').classes('absolute top-1/2 left-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_forward').classes('absolute top-1/2 right-2')

    with ui.tab_panel('B') as tabB:
        ui.label('Content of B').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[1]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_back').classes('absolute top-1/2 left-2')

    with ui.tab_panel('C') as tabC:
        ui.label('Content of C').classes('text-center')
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[2]).classes('w-full h-full')
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_back').classes('absolute top-1/2 left-2')

ui.run()