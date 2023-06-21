from nicegui import ui

# define a list of URLs to be used as the image source in the UI
image_urls = [
    'https://picsum.photos/300/300?1',
    'https://picsum.photos/300/300?2',
    'https://picsum.photos/300/300?3',
]

# create a dictionary to store the tab panels
tabs = {}

# function to switch tab panels


def switch_tab(value):
    tabs['panels'].value = value


# create tab_bar object without rendering it in the UI
tab_bar = ui.tabs()

# create a footer that is initially hidden
with ui.footer(value=False) as footer:
    ui.label('Footer')  # add a label to the footer

# create a sticky button in the bottom-right of the page to toggle the footer
with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

# create tab panels associated with the tab_bar
with ui.tab_panels(tab_bar, value='A').classes('w-full') as panels:
    tabs['panels'] = panels

    # define the first tab panel 'A'
    with ui.tab_panel('A') as tabA:
        ui.label('Content of A').classes('text-center')  # add a centered label
        # create a card with image and navigation buttons
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[0]).classes('w-full h-full')  # display image
                # create navigation buttons to switch between tab panels
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_back').classes('absolute top-1/2 left-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_forward').classes('absolute top-1/2 right-2')

    # define the second tab panel 'B'
    with ui.tab_panel('B') as tabB:
        ui.label('Content of B').classes('text-center')  # add a centered label
        # create a card with image and navigation buttons
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[1]).classes('w-full h-full')  # display image
                # create navigation buttons to switch between tab panels
                ui.button(on_click=lambda: switch_tab('C'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_back').classes('absolute top-1/2 left-2')

    # define the third tab panel 'C'
    with ui.tab_panel('C') as tabC:
        ui.label('Content of C').classes('text-center')  # add a centered label
        # create a card with image and navigation buttons
        with ui.card().classes('m-4 p-4 shadow-lg w-128 h-64 relative'):
            with ui.card().classes('w-full h-full absolute'):
                ui.image(image_urls[2]).classes('w-full h-full')  # display image
                # create navigation buttons to switch between tab panels
                ui.button(on_click=lambda: switch_tab('A'), icon='arrow_forward').classes('absolute top-1/2 right-2')
                ui.button(on_click=lambda: switch_tab('B'), icon='arrow_back').classes('absolute top-1/2 left-2')

# run the UI
ui.run()
