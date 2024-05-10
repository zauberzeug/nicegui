import os
from typing import Dict

from pydantic import BaseModel, Field

from nicegui import ui
from nicegui.page_layout import LeftDrawer


# --- Load service data for fake cloud provider portal

class SubServiceDefinition(BaseModel):
    title: str = Field(..., description='The title of the sub-service', examples=['Digital Twin'])
    emoji: str = Field(..., description='An emoji representing the sub-service', examples=['🤖'])
    description: str = Field(..., description='A short description of the sub-service',
                             examples=['Manage your digital twin'])


class ServiceDefinition(BaseModel):
    title: str = Field(..., description='The title of the cloud service', examples=['Virtual Machines'])
    emoji: str = Field(..., description='An emoji representing the cloud service', examples=['💻'])
    description: str
    sub_services: Dict[str, SubServiceDefinition]


class ServiceDefinitions(BaseModel):
    services: Dict[str, ServiceDefinition]


services = ServiceDefinitions.parse_file(os.path.join(os.path.dirname(__file__), 'services.json')).services


# --- Other app ---

@ui.outlet('/other_app')  # Needs to be defined before the main outlet / to avoid conflicts
def other_app_router():
    ui.label('Other app header').classes('text-h2')
    ui.html('<hr>')
    yield
    ui.html('<hr>')
    ui.label('Other app footer')


@other_app_router.view('/')
def other_app_index():
    ui.label('Welcome to the index page of the other application')


# --- Main app ---

@ui.outlet('/')  # main app outlet
def main_router(url_path: str):
    with ui.header():
        with ui.link('', '/').style('text-decoration: none; color: inherit;') as lnk:
            ui.html('<span style="color:white">Nice</span>'
                    '<span style="color:black">CLOUD</span>').classes('text-h3')
    menu_visible = '/services/' in url_path  # the service will make the menu visible anyway - suppresses animation
    menu_drawer = ui.left_drawer(bordered=True, value=menu_visible, fixed=True).classes('bg-primary')
    with ui.footer():
        ui.label('Copyright 2024 by My Company')

    with ui.element().classes('p-8'):
        yield {'menu_drawer': menu_drawer}  # pass menu drawer to all sub elements (views and outlets)


@main_router.view('/')
def main_app_index(menu_drawer: LeftDrawer):  # main app index page
    menu_drawer.clear()  # clear drawer
    menu_drawer.hide()  # hide drawer
    ui.label('Welcome to NiceCLOUD!').classes('text-3xl')
    ui.html('<br>')
    with ui.grid(columns=3) as grid:
        grid.classes('gap-16')
        for key, info in services.items():
            link = f'/services/{key}'
            with ui.element():
                with ui.link(target=link) as lnk:
                    with ui.row().classes('text-2xl'):
                        ui.label(info.emoji)
                        ui.label(info.title)
                    lnk.style('text-decoration: none; color: inherit;')
                ui.label(info.description)

    ui.html('<br><br>')
    # add a link to the other app
    ui.markdown("Click [here](/other_app) to visit the other app.")


@main_router.outlet('/services/{service_name}')  # service outlet
def services_router(service_name: str, menu_drawer: LeftDrawer):
    service: ServiceDefinition = services[service_name]
    # update menu drawer
    menu_drawer.clear()
    with menu_drawer:
        menu_drawer.show()
        with ui.row() as row:
            ui.label(service.emoji)
            ui.label(service.title)
            row.classes('text-h5 text-white').style('text-shadow: 2px 2px #00000070;')
        ui.html('<br>')
        menu_items = service.sub_services
        for key, info in menu_items.items():
            with ui.row() as service_element:
                ui.label(info.emoji)
                ui.label(info.title)
                service_element.classes('text-white text-h6 bg-gray cursor-pointer')
                service_element.style('text-shadow: 2px 2px #00000070;')
                service_element.on('click', lambda url=f'/services/{service_name}/{key}': ui.navigate.to(url))
    yield {'service': service}  # pass service to all sub elements (views and outlets)


@services_router.view('/')  # service index page
def show_index(service: ServiceDefinition):
    with ui.row() as row:
        ui.label(service.emoji).classes('text-h4 vertical-middle')
        with ui.column():
            ui.label(service.title).classes('text-h2')
            ui.label(service.description)
    ui.html('<br>')


@services_router.outlet('/{sub_service_name}')  # sub service outlet
def sub_service_router(service: ServiceDefinition, sub_service_name: str):
    sub_service: SubServiceDefinition = service.sub_services[sub_service_name]
    ui.label(f'{service.title} > {sub_service.title}').classes('text-h4')
    ui.html('<br>')
    yield {'sub_service': sub_service}  # pass sub service to all sub elements (views and outlets)


@sub_service_router.view('/')  # sub service index page
def sub_service_index(sub_service: SubServiceDefinition):
    ui.label(sub_service.emoji).classes('text-h1')
    ui.html('<br>')
    ui.label(sub_service.description)


ui.run(show=False)
