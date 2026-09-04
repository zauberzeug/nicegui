#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

from fullcalendar import FetchInfoArguments, FullCalendar as fullcalendar

from nicegui import events, ui

EVENTS_FILE = Path(__file__).parent / 'events_data' / 'events_full.json'

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
    'initialDate': '2026-09-01',
    'events': lambda *args, **kwargs: None,
}


def handle_click(event: events.GenericEventArguments):
    if 'info' in event.args:
        ui.notify(event.args['info']['event'])


def handle_fetch(info: FetchInfoArguments) -> None:
    start_ms = info.start_value
    end_ms = info.end_value
    all_events = json.loads(EVENTS_FILE.read_text(encoding='utf-8'))
    filtered = [
        e for e in all_events
        if _event_intersects_range(e, start_ms, end_ms)
    ]
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
