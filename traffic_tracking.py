import logging
import os
import pickle
import threading
import time
from typing import Dict, Set

from starlette.requests import Request

from nicegui import ui

VISITS_FILE = 'traffic_data/visits.pickle'
SESSIONS_FILE = 'traffic_data/sessions.pickle'

visits: Dict[int, int] = {}
sessions: Dict[int, Set[str]] = {}

os.makedirs(os.path.dirname(VISITS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
try:
    with open(VISITS_FILE, 'rb') as f:
        visits = pickle.load(f)
    with open(SESSIONS_FILE, 'rb') as f:
        sessions = pickle.load(f)
except FileNotFoundError:
    pass
except:
    logging.exception('Error loading traffic data')


def keep_backups(self) -> None:
    def _save() -> None:
        try:
            with open(VISITS_FILE, 'wb') as f:
                pickle.dump(visits, f)
            with open(SESSIONS_FILE, 'wb') as f:
                pickle.dump(sessions, f)
        except:
            logging.exception('Error saving traffic data')

    while True:
        time.sleep(10)
        t = threading.Thread(target=_save, name='Save Traffic Data')
        t.start()


class TrafficChart(ui.chart):

    def __init__(self) -> None:

        ui.on_connect(self.on_connect)
        ui.timer(10, self.update_visibility)

        super().__init__({
            'title': {'text': 'Page Visits'},
            'navigation': {'buttonOptions': {'enabled': False}},
            'chart': {'type': 'line'},
            'yAxis': {'title': False, 'type': 'logarithmic', },
            'xAxis': {
                'type': 'datetime',
                'labels': {'format': '{value:%b %e}', },
            },
            'series': [
                {'name': 'Views', 'data': []},
                {'name': 'Sessions', 'data': []},
            ],
        })

    def on_connect(self, request: Request) -> None:
        # ignore monitoring, web crawlers and the like
        agent = request.headers['user-agent'].lower()
        if any(s in agent for s in ('bot', 'spider', 'crawler', 'monitor', 'curl', 'wget', 'python-requests', 'kuma')):
            return

        def seconds_to_day(seconds: float) -> int: return int(seconds / 60 / 60 / 24)
        def day_to_milliseconds(day: int) -> float: return day * 24 * 60 * 60 * 1000
        today = seconds_to_day(time.time())
        visits[today] = visits.get(today, 0) + 1
        self.options.series[0].data[:] = [[day_to_milliseconds(day), count] for day, count in visits.items()]
        # remove first day because data are inconclusive depending on deployment time
        self.options.series[0].data[:] = self.options.series[0].data[1:]
        if today not in sessions:
            sessions[today] = set()
        sessions[today].add(request.session_id)
        self.options.series[1].data[:] = [[day_to_milliseconds(day), len(s)] for day, s in sessions.items()]
        # remove first day because data are inconclusive depending on deployment time
        self.options.series[1].data[:] = self.options.series[1].data[1:]
        self.update()

    def update_visibility(self) -> None:
        self.visible = len(visits.keys()) >= 3 and len(sessions.keys()) >= 3
