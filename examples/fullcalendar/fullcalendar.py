from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from nicegui.element import Element
from nicegui.events import handle_event


class FullCalendar(Element, component='fullcalendar.js'):
    """
    An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar display.

    - options: dictionary of FullCalendar properties for customization, such as "initialView", "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", and "events".
    :type options: dict
    - on_click: callback function that is called when a calendar event is clicked.
    :type on_click: Optional[Callable]
    """

    def __init__(self, options: Dict[str, Any], on_click: Optional[Callable] = None) -> None:
        """
        Initialize the FullCalendar element.

        - options: dictionary of FullCalendar properties for customization.
        :type options: dict
        - on_click: callback function that is called when a calendar event is clicked.
        :type on_click: Optional[Callable]
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib')
        self._props['options'] = options

        if on_click:
            self.on('click', lambda e: handle_event(on_click, e))

    def add_event(self, title: str, start: str, end: str, **kwargs) -> None:
        """
        Add an event to the calendar.

        - title: title of the event
        :type title: str
        - start: start time of the event
        :type start: str
        - end: end time of the event
        :type end: str
        """
        event_dict = {'title': title, 'start': start, 'end': end, **kwargs}
        self._props['options']['events'].append(event_dict)
        self.update()
        self.run_method('update_calendar')

    def remove_event(self, title: str, start: str, end: str) -> None:
        """
        Remove an event from the calendar.

        - title: title of the event
        :type title: str
        - start: start time of the event
        :type start: str
        - end: end time of the event
        :type end: str
        """
        for event in self._props['options']['events']:
            if event['title'] == title and event['start'] == start and event['end'] == end:
                self._props['options']['events'].remove(event)
                break

        self.update()
        self.run_method('update_calendar')

    @property
    def events(self) -> List[Dict]:
        """
        List of events currently displayed in the calendar.

        :return: list of event dictionaries
        :rtype: List[Dict]
        """
        return self._props['options']['events']
