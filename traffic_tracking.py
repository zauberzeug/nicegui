import logging
import os
import pickle
import threading
import time
from typing import Dict, Set

from starlette.requests import Request

from nicegui import ui

page_visits: Dict[int, int] = {}
page_sessions: Dict[int, Set[str]] = {}


def add_chart() -> ui.chart:

    def on_connect(request: Request):
        factor = 60 * 24
        today = int(time.time() / factor)
        page_visits[today] = page_visits.get(today, 0) + 1
        traffic_chart.options.series[0].data[:] = [[day * factor * 1000, count] for day, count in page_visits.items()]
        if not today in page_sessions:
            page_sessions[today] = set()
        page_sessions[today].add(request.session_id)
        traffic_chart.options.series[1].data[:] = [[day * factor * 1000, len(s)] for day, s in page_sessions.items()]
        traffic_chart.update()

    ui.on_connect(on_connect)
    ui.timer(10, save)
    load()
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

    traffic_chart.visible = len(page_visits.keys) > 2 and len(page_sessions.keys) > 2
    return traffic_chart


def load() -> None:
    global page_visits, page_sessions
    try:
        with open('page_visits.pickle', 'rb') as f:
            page_visits = pickle.load(f)
        with open('page_sessions.pickle', 'rb') as f:
            page_sessions = pickle.load(f)
    except FileNotFoundError:
        pass
    except:
        logging.exception("Error loading traffic data")


def save() -> None:
    def _save():
        try:
            with open('page_visits.pickle', 'wb') as f:
                pickle.dump(page_visits, f)
            with open('page_sessions.pickle', 'wb') as f:
                pickle.dump(page_sessions, f)
        except:
            logging.exception("Error saving traffic data")

    t = threading.Thread(target=_save, name="Save Traffic Data")
    t.start()
