# Basic example of the SinglePageApp class which allows the fast conversion of already existing multi-page NiceGUI
# applications into a single page applications. Note that if you want more control over the routing, nested outlets or
# custom page setups,you should use the ui.outlet class instead which allows more flexibility.

from nicegui import ui
from nicegui.page import page
from nicegui.single_page_app import SinglePageApp


@page('/', title='Welcome!')
def index():
    ui.label('Welcome to the single page router example!')
    ui.link('About', '/about')


@page('/about', title='About')
def about():
    ui.label('This is the about page')
    ui.link('Index', '/')


def page_template():
    with ui.header():
        ui.label('My Company').classes('text-2xl')
    yield  # your content goes here


router = SinglePageApp('/', page_template=page_template).setup()
ui.run()
