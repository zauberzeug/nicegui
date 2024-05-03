# Minimal example of a single page router with two pages

from nicegui import ui
from nicegui.page import page
from nicegui.single_page_app import SinglePageApp
from nicegui.single_page_router import SinglePageRouter


@page('/', title='Welcome!')
def index():
    ui.label('Welcome to the single page router example!')
    ui.link('About', '/about')


@page('/about', title='About')
def about():
    ui.label('This is the about page')
    ui.link('Index', '/')


router = SinglePageApp('/').reroute_pages()
ui.run()
