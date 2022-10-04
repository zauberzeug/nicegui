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
REFERRERS_FILE = 'traffic_data/referrers.pickle'

visits: Dict[int, int] = {}
sessions: Dict[int, Set[str]] = {}
referrers: Dict[int, Dict[str, int]] = {}

os.makedirs(os.path.dirname(VISITS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(REFERRERS_FILE), exist_ok=True)
try:
    with open(VISITS_FILE, 'rb') as f:
        visits = pickle.load(f)
    with open(SESSIONS_FILE, 'rb') as f:
        sessions = pickle.load(f)
    with open(REFERRERS_FILE, 'rb') as f:
        referrers = pickle.load(f)
except FileNotFoundError:
    pass
except:
    logging.exception('Error loading traffic data')

should_exit = threading.Event()


def keep_backups() -> None:
    def _save() -> None:
        while not should_exit.is_set():
            try:
                with open(VISITS_FILE, 'wb') as f:
                    pickle.dump(visits, f)
                with open(SESSIONS_FILE, 'wb') as f:
                    pickle.dump(sessions, f)
                with open(REFERRERS_FILE, 'wb') as f:
                    pickle.dump(referrers, f)
            except:
                logging.exception('Error saving traffic data')
            time.sleep(1)

    t = threading.Thread(target=_save, name='Save Traffic Data')
    t.start()


ui.on_startup(keep_backups)
ui.on_shutdown(should_exit.set)


def on_connect(request: Request) -> None:
    # ignore monitoring, web crawlers and the like
    agent = request.headers['user-agent'].lower()
    if any(s in agent for s in ('bot', 'spider', 'crawler', 'monitor', 'curl', 'wget', 'python-requests', 'kuma')):
        return
    origin_url = request.headers.get('referer', 'unknown')
    print(f'new connection from {agent}, coming from {origin_url}', flush=True)
    def seconds_to_day(seconds: float) -> int: return int(seconds / 60 / 60 / 24)
    #print(f'traffic data: {[datetime.fromtimestamp(day_to_milliseconds(t)/1000) for t in visits.keys()]}')
    today = seconds_to_day(time.time())
    visits[today] = visits.get(today, 0) + 1
    referrers[today] = referrers.get(today, {})
    referrers[today][origin_url] = referrers[today].get(origin_url, 0) + 1
    print(referrers, flush=True)
    if today not in sessions:
        sessions[today] = set()
    sessions[today].add(request.session_id)


class chart(ui.chart):

    def __init__(self) -> None:
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
        self.visible = len(visits.keys()) >= 3 and len(sessions.keys()) >= 3
        ui.timer(10, self.update)

    def update(self) -> None:
        def day_to_milliseconds(day: int) -> float: return day * 24 * 60 * 60 * 1000
        self.options.series[0].data[:] = [[day_to_milliseconds(day), count] for day, count in visits.items()]
        # remove first day because data are inconclusive depending on deployment time
        self.options.series[0].data[:] = self.options.series[0].data[1:]

        self.options.series[1].data[:] = [[day_to_milliseconds(day), len(s)] for day, s in sessions.items()]
        # remove first day because data are inconclusive depending on deployment time
        self.options.series[1].data[:] = self.options.series[1].data[1:]
        super().update()
