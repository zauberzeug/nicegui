# Advanced example of a single page router which includes a custom router class and a custom root page setup
# with static footer, header and menu elements.
from typing import Callable

from nicegui import ui
from nicegui.page import page
from nicegui.single_page import SinglePageRouter


def setup_page_layout(content: Callable):
    with ui.header():
        ui.label('My Company').classes('text-2xl')
    with ui.left_drawer():
        ui.button('Home', on_click=lambda: ui.navigate.to('/'))
        ui.button('About', on_click=lambda: ui.navigate.to('/about'))
        ui.button('Contact', on_click=lambda: ui.navigate.to('/contact'))
    content()  # <-- The individual pages will be rendered here
    with ui.footer() as footer:
        ui.label('Copyright 2023 by My Company')


@page('/', title='Welcome!')
def index():
    ui.label('Welcome to the single page router example!').classes('text-2xl')


@page('/about', title='About')
def about():
    ui.label('This is the about page testing local references').classes('text-2xl')
    ui.label('Top').classes('text-lg').props('id=ltop')
    ui.link('Bottom', '#lbottom')
    ui.link('Center', '#lcenter')
    for i in range(30):
        ui.label(f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. {i}')
    ui.label('Center').classes('text-lg').props('id=lcenter')
    ui.link('Top', '#ltop')
    ui.link('Bottom', '#lbottom')
    for i in range(30):
        ui.label(f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. {i}')
    ui.label('Bottom').classes('text-lg').props('id=lbottom')
    ui.link('Top', '#ltop')
    ui.link('Center', '#lcenter')


@page('/contact', title='Contact')  # this page will not be hosted as SPA
def contact():
    def custom_content_area():
        ui.label('This is the contact page').classes('text-2xl')

    setup_page_layout(content=custom_content_area)


class CustomRouter(SinglePageRouter):
    def setup_root_page(self, **kwargs):
        setup_page_layout(content=self.setup_content_area)


router = CustomRouter('/', included=[index, about], excluded=[contact])
router.setup_page_routes()
ui.run()
