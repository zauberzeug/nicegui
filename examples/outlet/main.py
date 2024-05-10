import json
import os.path

from nicegui import ui

# load service definition file of imaginary cloud services
services = json.load(open(os.path.dirname(__file__) + '/services.json'))


@ui.outlet('/other_app')
def other_app():
    ui.label('Other app header').classes('text-h2')
    ui.html('<hr>')
    yield
    ui.html('<hr>')
    ui.label('Other app footer')


@other_app.view('/')
def other_app_index():
    ui.label('Welcome to the index page of the other application')


@ui.outlet('/')
def main_router():
    with ui.header():
        with ui.link("", '/') as lnk:
            ui.html('<span style="color:white">Nice</span>'
                    '<span style="color:black">CLOUD</span>').classes('text-h3')
            lnk.style('text-decoration: none; color: inherit;')
    with ui.footer():
        ui.label("Copyright 2024 by My Company")

    with ui.element().classes('p-8'):
        yield


@main_router.view('/')
def main_app_index():
    ui.label("Welcome to NiceCLOUD!").classes('text-3xl')
    ui.html("<br>")
    with ui.grid(columns=3) as grid:
        grid.classes('gap-8')
        for key, info in services.items():
            link = f'/services/{key}'
            with ui.element():
                with ui.row():
                    ui.label(info['emoji']).classes('text-2xl')
                    with ui.link("", link) as lnk:
                        ui.label(info['title']).classes('text-2xl')
                        lnk.style('text-decoration: none; color: inherit;')
                ui.label(info['description'])

    ui.html("<br><br>")
    # add a link to the other app
    ui.link("Other App", '/other_app')


@main_router.outlet('/services/{service_name}')
def services_router(service_name: str):
    service_config = services[service_name]
    with ui.left_drawer(bordered=True) as menu_drawer:
        menu_drawer.classes('bg-primary')
        title = service_config['title']
        ui.label(title).classes('text-2xl text-white')
        # add menu items
        menu_items = service_config['sub_services']
        for key, info in menu_items.items():
            title = info['title']
            with ui.button(title) as btn:
                btn.classes('text-white bg-secondary').on_click(lambda sn=service_name, k=key:
                                                                ui.navigate.to(f'/services/{sn}/{k}'))

    yield {'service': services[service_name]}


@services_router.outlet('/{sub_service_name}')
def sub_service(service, sub_service_name: str):
    service_title = service['title']
    sub_service = service["sub_services"][sub_service_name]
    ui.label(f'{service_title} > {sub_service["title"]}').classes('text-h4')
    ui.html("<br>")
    yield {'sub_service': sub_service}


@sub_service.view('/')
def sub_service_index(sub_service):
    ui.label(sub_service["description"])


@services_router.view('/')
def show_index(service_name, **kwargs):
    service_info = services[service_name]
    ui.label(service_info["title"]).classes("text-h2")
    ui.html("<br>")
    ui.label(service_info["description"])


ui.run(show=False)
