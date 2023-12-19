from nicegui import ui

from . import doc


@doc.demo(ui.fullcalendar)
def main_demo() -> None:
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
        'events': [],
    }
    ui.fullcalendar(options, on_click=ui.notify)


doc.reference(ui.fullcalendar)
