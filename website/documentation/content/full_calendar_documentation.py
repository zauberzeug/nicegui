from nicegui import ui

from . import doc


@doc.demo(ui.fullcalendar)
def main_demo() -> None:
    from datetime import datetime

    def format_date(dt: datetime) -> str:
        """Parse the date string and format it consistently."""
        return dt.strftime(r'%Y-%m-%d %H:%M:%S')

    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js"></script>')
    options = {
        'initialView': 'timeGridWeek',
        'slotMinTime': '05:00:00',
        'slotMaxTime': '22:00:00',
        'allDaySlot': False,
        'timeZone': 'local',
        'height': 'auto',
        'width': 'auto',
        'events': [],
    }
    calendar = ui.fullcalendar(options, on_click=ui.notify)
    calendar.add_event('Math 1b03', format_date(datetime.now()), format_date(datetime.now()), color='red')
