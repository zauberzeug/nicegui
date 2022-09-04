import os
import time

from starlette.requests import Request

from nicegui import ui


def add() -> ui.chart:
    page_visits: dict[int, int] = {}
    page_sessions: dict[int, set[str]] = {}

    def handle_connection(request: Request):
        factor = 60 * 24
        today = int(time.time() / factor)
        page_visits[today] = page_visits.get(today, 0) + 1
        traffic_chart.options.series[0].data[:] = [[day * factor * 1000, count]
                                                   for day, count in page_visits.items()]
        if not today in page_sessions:
            page_sessions[today] = set()
        page_sessions[today].add(request.session_id)
        traffic_chart.options.series[1].data[:] = [
            [day * factor * 1000, len(s)] for day, s in page_sessions.items()]
        traffic_chart.update()

    ui.on_connect(handle_connection)

    traffic_chart = ui.chart({
        'title': {'text': 'Traffic'},
        'navigation': {'buttonOptions': {'enabled': False}},
        'chart': {'type': 'line'},
        'yAxis': {'title': False},
        'xAxis': {
            'type': 'datetime',
            'labels': {'format': '{value:%e. %b}', },
        },
        'series': [
            {'name': 'Views', 'data': []},
            {'name': 'Sessions', 'data': []},
        ],
    })

    traffic_chart.visible = os.environ.get('SHOW_TRAFFIC')
    return traffic_chart
