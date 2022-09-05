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


class TrafficChard(ui.chart):

    def __init__(self) -> None:
        self.visits: Dict[int, int] = {}
        self.sessions: Dict[int, Set[str]] = {}
        self.load()

        ui.on_connect(self.on_connect)
        ui.timer(10, self.save)
        ui.timer(10, self.update_visibility)

        super().__init__({
            'title': {'text': 'Page Visits'},
            'navigation': {'buttonOptions': {'enabled': False}},
            'chart': {'type': 'line'},
            'yAxis': {'title': False},
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
        def seconds_to_day(seconds: float) -> int: return int(seconds / 60 / 60 / 24)
        def day_to_milliseconds(day: int) -> float: return day * 24 * 60 * 60 * 1000
        today = seconds_to_day(time.time())
        self.visits[today] = self.visits.get(today, 0) + 1
        self.options.series[0].data[:] = [[day_to_milliseconds(day), count] for day, count in self.visits.items()]
        if today not in self.sessions:
            self.sessions[today] = set()
        self.sessions[today].add(request.session_id)
        self.options.series[1].data[:] = [[day_to_milliseconds(day), len(s)] for day, s in self.sessions.items()]
        self.update()

    def load(self) -> None:
        os.makedirs(os.path.dirname(VISITS_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
        try:
            with open(VISITS_FILE, 'rb') as f:
                self.visits = pickle.load(f)
            with open(SESSIONS_FILE, 'rb') as f:
                self.sessions = pickle.load(f)
        except FileNotFoundError:
            pass
        except:
            logging.exception('Error loading traffic data')

    def save(self) -> None:
        def _save() -> None:
            try:
                with open(VISITS_FILE, 'wb') as f:
                    pickle.dump(self.visits, f)
                with open(SESSIONS_FILE, 'wb') as f:
                    pickle.dump(self.sessions, f)
            except:
                logging.exception('Error saving traffic data')

        t = threading.Thread(target=_save, name='Save Traffic Data')
        t.start()

    def update_visibility(self) -> None:
        self.visible = True  # len(self.visits.keys()) >= 3 and len(self.sessions.keys()) >= 3
