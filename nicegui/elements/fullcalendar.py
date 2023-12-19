from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..element import Element
from ..events import handle_event


class FullCalendar(Element, component='fullcalendar.js'):

    def __init__(self, options: Dict[str, Any], on_click: Optional[Callable] = None) -> None:
        """FullCalendar

        An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar display.

        :param options: dictionary of FullCalendar properties for customization, such as "initialView", "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", and "events".
        :param on_click: callback function that is called when a calendar event is clicked.
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'fullcalendar')
        self._props['options'] = options

        if on_click:
            self.on('click', lambda e: handle_event(on_click, e))

    def add_event(self, title: str, start: str, end: str, **kwargs) -> None:
        event_dict = {'title': title, 'start': start, 'end': end, **kwargs}
        self._props['options']['events'].append(event_dict)
        self.update()
        self.run_method('update_calendar')

    def remove_event(self, title: str, start: str, end: str) -> None:
        for event in self._props['options']['events']:
            if event['title'] == title and event['start'] == start and event['end'] == end:
                self._props['options']['events'].remove(event)
                break

        self.update()
        self.run_method('update_calendar')

    @property
    def events(self) -> List[Dict]:
        return self._props['options']['events']
