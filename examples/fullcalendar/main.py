#!/usr/bin/env python3
from datetime import datetime

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
    'events': [
        {
            'title': 'Math',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 08:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
            'color': 'red',
        },
        {
            'title': 'Physics',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 12:00:00',
            'color': 'green',
        },
        {
            'title': 'Chemistry',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 13:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 15:00:00',
            'color': 'blue',
        },
        {
            'title': 'Biology',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 15:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 17:00:00',
            'color': 'orange',
        },
    ],
}


def handle_click(event: events.GenericEventArguments):
    if 'info' in event.args:
        ui.notify(event.args['info']['event'])


fullcalendar(options, on_click=handle_click)

ui.run()
