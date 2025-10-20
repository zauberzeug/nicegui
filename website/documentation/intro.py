import random
from typing import Callable

from nicegui import ui

from ..style import subheading
from .content.sub_pages_documentation import FakeSubPages
from .demo import demo


def create_intro() -> None:
    @_main_page_demo('Single-Page Applications', '''
        Build applications with fast client-side routing using [`ui.sub_pages`](/documentation/sub_pages)
        and a `root` function as single entry point.
        For each visitor, the `root` function is executed and generates the interface.
        [`ui.link`](/documentation/link) and [`ui.navigate`](/documentation/navigate) can be used to navigate to other sub pages.

        If you do not want a single-page application, you can also use [`@ui.page('/your/path')`](/documentation/page)
        to define standalone content available at a specific path.
    ''')
    def spa_demo():
        sub_pages = None  # HIDE

        def root():
            # ui.sub_pages({
            #     '/': table_page,
            #     '/map/{lat}/{lon}': map_page,
            # }).classes('w-full')
            nonlocal sub_pages  # HIDE
            sub_pages = FakeSubPages({'/': table_page, '/map/{lat}/{lon}': map_page}).classes('w-full')  # HIDE
            sub_pages.init()  # HIDE

        def table_page():
            ui.table(rows=[
                {'name': 'New York', 'lat': 40.7119, 'lon': -74.0027},
                {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
                {'name': 'Tokio', 'lat': 35.6863, 'lon': 139.7722},
            ]).on('row-click', lambda e: sub_pages._render('/map/{lat}/{lon}', lat=e.args[1]['lat'], lon=e.args[1]['lon']))  # HIDE
            # ]).on('row-click', lambda e: ui.navigate.to(f'/map/{e.args[1]["lat"]}/{e.args[1]["lon"]}'))

        def map_page(lat: float, lon: float):
            ui.leaflet(center=(lat, lon), zoom=10)
            # ui.link('Back to table', '/')
            sub_pages.link('Back to table', '/')  # HIDE

        return root

    @_main_page_demo('Reactive Transformations', '''
        Create real-time interfaces with automatic updates.
        Type and watch text flow in both directions.
        When input changes, the [binding](/documentation/section_binding_properties) transforms the text
        with a custom Python function and updates the label.
    ''')
    def binding_demo():
        def root():
            user_input = ui.input(value='Hello')
            ui.label().bind_text_from(user_input, 'value', reverse)

        def reverse(text: str) -> str:
            return text[::-1]

        return root

    @_main_page_demo('Event System', '''
        Use an [Event](/documentation/event) to trigger actions and pass data.
        Here we have an IoT temperature sensor submitting its readings
        to a [FastAPI endpoint](/documentation/section_pages_routing#api_responses) with path "/sensor".
        When a new value arrives, it emits an event for the chart to be updated.
    ''')
    def event_system_demo():
        import time

        from nicegui import Event, app

        sensor = Event[float]()

        # @app.post('/sensor')
        def sensor_webhook(temperature: float):
            sensor.emit(temperature)

        def root():
            chart = ui.echart({
                'xAxis': {'type': 'time', 'axisLabel': {'hideOverlap': True}},
                'yAxis': {'type': 'value', 'min': 'dataMin'},
                'series': [{'type': 'line', 'data': [], 'smooth': True}],
            })

            def update_chart(temperature: float):
                data = chart.options['series'][0]['data']
                data.append([time.time(), temperature])
                if len(data) > 10:
                    data.pop(0)

            sensor.subscribe(update_chart)
            # END OF DEMO

            data = chart.options['series'][0]['data']
            data.append([time.time(), 24.0])
            ui.timer(1.0, lambda: update_chart(round(data[-1][1] + (random.random() - 0.5), 1)), immediate=False)
        app  # noqa: B018 to avoid unused import warning

        return root


def _main_page_demo(title: str, explanation: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        subheading(title)
        ui.markdown(explanation).classes('bold-links arrow-links')
        return demo(f)
    return decorator
