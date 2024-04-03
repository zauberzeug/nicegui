# Advanced example of a single page router which includes a custom router class and a custom root page setup
# with static footer, header and menu elements.

from nicegui import ui
from nicegui.page import page
from nicegui.single_page import SinglePageRouter


class CustomRouter(SinglePageRouter):
    def setup_root_page(self):
        with ui.header():
            ui.label("My Company").classes("text-2xl")
        with ui.left_drawer():
            ui.button("Home", on_click=lambda: ui.navigate.to("/"))
            ui.button("About", on_click=lambda: ui.navigate.to("/about"))
        self.setup_content_area()  # <-- The individual pages will be rendered here
        with ui.footer() as footer:
            ui.label("Copyright 2023 by My Company")


@page('/', title="Welcome!")
def index():
    ui.label("Welcome to the single page router example!").classes("text-2xl")


@page('/about', title="About")
def about():
    ui.label("This is the about page").classes("text-2xl")


router = CustomRouter("/").setup_page_routes()
ui.run()
