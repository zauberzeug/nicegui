# Advanced demo showing how to use the ui.outlet and outlet.view decorators to create a nested multi-page app with a
# static header, footer and menu which is shared across all pages and hidden when the user navigates to the root page.

from nicegui import ui
from nicegui.page_layout import LeftDrawer
from nicegui.single_page_router import SinglePageRouter

from examples.single_page_app_complex.cms_config import SubServiceDefinition, ServiceDefinition, services


# --- Other app ---

@ui.outlet('/other_app')  # Needs to be defined before the main outlet / to avoid conflicts
async def other_app_router():
    ui.label('Other app header').classes('text-h2')
    ui.html('<hr>')
    yield
    ui.html('<hr>')
    ui.label('Other app footer')


@other_app_router.view('/')
async def other_app_index():
    ui.label('Welcome to the index page of the other application')


# --- Main app ---

@ui.outlet('/')  # main app outlet
async def main_router(url_path: str):
    with ui.header():
        with ui.link('', '/').style('text-decoration: none; color: inherit;') as lnk:
            ui.html('<span style="color:white">Nice</span>'
                    '<span style="color:black">CLOUD</span>').classes('text-h3')
    menu_visible = '/services/' in url_path  # make instantly visible if the initial path is a service
    menu_drawer = ui.left_drawer(bordered=True, value=menu_visible, fixed=True).classes('bg-primary')
    with ui.footer():
        with ui.element('a').props('href="/about"'):
            ui.label('Copyright 2024 by NiceCLOUD Inc.').classes('text-h7')
    with ui.element().classes('p-8'):
        yield {'menu_drawer': menu_drawer}  # pass menu drawer to all sub elements (views and outlets)


@main_router.view('/')
async def main_index(menu_drawer: LeftDrawer):  # main app index page
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
    ui.markdown('Click [here](/other_app) to visit the other app.')


@main_router.view('/about')
async def about_page(menu_drawer: LeftDrawer):
    menu_drawer.clear()
    menu_drawer.hide()
    ui.label('About NiceCLOUD').classes('text-3xl')
    ui.html('<br>')
    ui.label('NiceCLOUD Inc.')
    ui.label('1234 Nice Street')
    ui.label('Nice City')
    ui.label('Nice Country')


@main_router.outlet('/services/{service_name}')  # service outlet
async def services_router(service_name: str, menu_drawer: LeftDrawer):
    service: ServiceDefinition = services[service_name]
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
    yield {'service': service}  # pass service object to all sub elements (views and outlets)


def update_title(service: ServiceDefinition = None,
                 sub_service: SubServiceDefinition = None):
    new_title = \
            'NiceCLOUD - ' + (f'{sub_service.title}' if sub_service else f'{service.title}')
    ui.page_title(new_title)


@services_router.view('/')  # service index page
async def show_index(service: ServiceDefinition):
    update_title(service, None)
    with ui.row() as row:
        ui.label(service.emoji).classes('text-h4 vertical-middle')
        with ui.column():
            ui.label(service.title).classes('text-h2')
            ui.label(service.description)
    ui.html('<br>')


@services_router.outlet('/{sub_service_name}')  # sub service outlet
async def sub_service_router(service: ServiceDefinition, sub_service_name: str):
    sub_service: SubServiceDefinition = service.sub_services[sub_service_name]
    ui.label(f'{service.title} > {sub_service.title}').classes('text-h4')
    ui.html('<br>')
    yield {'sub_service': sub_service}  # pass sub_service object to all sub elements (views and outlets)


@sub_service_router.view('/')  # sub service index page
async def sub_service_index(service: ServiceDefinition, sub_service: SubServiceDefinition):
    update_title(service, sub_service)
    ui.label(sub_service.emoji).classes('text-h1')
    ui.html('<br>')
    ui.label(sub_service.description)


ui.run(title='NiceCLOUD Portal', show=False)
