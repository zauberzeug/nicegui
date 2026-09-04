#!/usr/bin/env python3
import random
from datetime import datetime, timedelta

from fullcalendar import FetchInfoArguments
from fullcalendar import FullCalendar as fullcalendar

from nicegui import events, ui

options = {
    'initialView': 'dayGridMonth',
    'headerToolbar': {'left': 'title', 'right': ''},
    'footerToolbar': {'right': 'prev,next today'},
    'slotMinTime': '05:00:00',
    'slotMaxTime': '22:00:00',
    'allDaySlot': False,
    'timeZone': 'local',
    'height': 'auto',
    'width': 'auto',
    'initialDate': datetime.now().strftime('%Y-%m-%d'),
    'events': lambda *args, **kwargs: None,
}

titles = [
    'Team meeting',
    'Project sync',
    'Design workshop',
    'Code review',
    'Sprint planning',
    'Client demo',
    'Internal training',
    'Maintenance',
    'Deployment',
    'Stand-up',
    'Retrospective',
    'Brainstorming',
]


def generate_events(year: int) -> list[dict[str, str]]:
    generator = random.Random(42)
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    generated_events = []
    for day in range((end_date - start_date).days + 1):
        current = start_date + timedelta(days=day)
        for _ in range(generator.randint(0, 3)):
            hour = generator.randint(8, 16)
            duration = generator.choice([1, 2])
            generated_events.append({
                'title': generator.choice(titles),
                'start': (current + timedelta(hours=hour)).isoformat(),
                'end': (current + timedelta(hours=hour + duration)).isoformat(),
                'color': generator.choice(['blue', 'green', 'red', 'orange', 'purple', 'teal']),
            })
    return generated_events


all_events = generate_events(datetime.now().year)


def handle_click(event: events.GenericEventArguments):
    if 'info' in event.args:
        ui.notify(event.args['info']['event'])


def handle_fetch(info: FetchInfoArguments) -> None:
    start_ms = info.start_value
    end_ms = info.end_value
    filtered = [e for e in all_events if _event_intersects_range(e, start_ms, end_ms)]
    ui.notify(f'Loaded {len(filtered)} events for range {info.start} → {info.end}')
    info.response(filtered)


def _event_intersects_range(event: dict, start_ms: int, end_ms: int) -> bool:
    event_start = _parse_local_ms(event['start'])
    event_end = _parse_local_ms(event.get('end', event['start']))
    return event_start < end_ms and event_end > start_ms


def _parse_local_ms(value: str) -> int:
    dt = datetime.fromisoformat(value)
    return int(dt.timestamp() * 1000)


fullcalendar(options, on_click=handle_click, on_fetch_events=handle_fetch)

ui.run()
