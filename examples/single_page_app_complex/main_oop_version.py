# Advanced demo showing how to use the ui.outlet and outlet.view decorators to create a nested multi-page app with a
# static header, footer and menu which is shared across all pages and hidden when the user navigates to the root page.

from nicegui import ui
from nicegui.single_page_router import SinglePageRouter
from examples.single_page_app_complex.cms_config import SubServiceDefinition, ServiceDefinition, services


# --- Other app ---

class OtherApp(SinglePageRouter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def other_app_index():
        ui.label('Welcome to the index page of the other application')

    @staticmethod
    def page_template():
        ui.label('Other app header').classes('text-h2')
        ui.html('<hr>')
        yield
        ui.html('<hr>')
        ui.label('Other app footer')


ui.outlet('/other_app', router_class=OtherApp)


# --- Main app ---

class MainAppInstance(SinglePageRouter):
    def __init__(self, menu_drawer, **kwargs):
        super().__init__(**kwargs)
        self.menu_drawer = menu_drawer
        self.add_view('/', self.index)
        self.add_view('/about', self.about_page, title='About NiceCLOUD')

    def index(self):  # main app index page
        self.menu_drawer.clear()  # clear drawer
        self.menu_drawer.hide()  # hide drawer
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

    def about_page(self):
        self.menu_drawer.clear()  # clear drawer
        self.menu_drawer.hide()  # hide drawer
        ui.label('About NiceCLOUD').classes('text-3xl')
        ui.html('<br>')
        ui.label('NiceCLOUD Inc.')
        ui.label('1234 Nice Street')
        ui.label('Nice City')
        ui.label('Nice Country')

    @staticmethod
    def page_template(url_path: str):
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


class ServicesRouter(SinglePageRouter):
    def __init__(self, service, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(self.parent, MainAppInstance)
        self.main_router: MainAppInstance = self.parent
        self.service = service
        self.add_view('/', self.show_index)

    def update_title(self):
        self.target.title = f'NiceCLOUD - {self.service.title}'

    def show_index(self):
        self.update_title()
        with ui.row() as row:
            ui.label(self.service.emoji).classes('text-h4 vertical-middle')
            with ui.column():
                ui.label(self.service.title).classes('text-h2')
                ui.label(self.service.description)
        ui.html('<br>')

    @staticmethod
    def page_template(service_name: str, menu_drawer):
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


class SubServiceRouter(SinglePageRouter):
    def __init__(self, sub_service, **kwargs):
        super().__init__(**kwargs)
        assert isinstance(self.parent, ServicesRouter)
        self.services_router: ServicesRouter = self.parent
        self.sub_service = sub_service
        self.add_view('/', self.sub_service_index)

    def update_title(self):
        self.target.title = f'NiceCLOUD - {self.sub_service.title}'

    def sub_service_index(self):
        self.update_title()
        ui.label(self.sub_service.emoji).classes('text-h1')
        ui.html('<br>')
        ui.label(self.sub_service.description)

    @staticmethod
    def page_template(service: ServiceDefinition, sub_service_name: str):
        sub_service: SubServiceDefinition = service.sub_services[sub_service_name]
        ui.label(f'{service.title} > {sub_service.title}').classes('text-h4')
        ui.html('<br>')
        yield {'sub_service': sub_service}  # pass sub_service object to all sub elements (views and outlets)


# main app outlet
main_router = ui.outlet('/', router_class=MainAppInstance)
# service outlet
services_router = main_router.outlet('/services/{service_name}', router_class=ServicesRouter)
# sub service outlet
sub_service_router = services_router.outlet('/{sub_service_name}', router_class=SubServiceRouter)

ui.run(title='NiceCLOUD Portal', show=False)
