from typing import Any, Callable, Dict, List, Optional

from ..element import Element
from ..events import GenericEventArguments, handle_event




class FullCalendar(Element, component='fullcalendar.js', libraries=['lib/fullcalendar/index.global.min.js']):
    def __init__(self, options: Dict[str, Any], on_click: Optional[Callable] = None) -> None:
        """ FullCalendar
            An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar display.
            
            
            :param properties: dictionary of FullCalendar properties for customization, such as "initialView", "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", and "events".
            :param on_click: callback function that is called when a calendar event is clicked.
            :return: FullCalendar element with the specified properties and event handling.
                
        """

        super().__init__()
        self._props['options'] = options
        
        if on_click:
            def handle_on_click(e: GenericEventArguments):
                handle_event(on_click, e)

            self.on("click", handle_on_click, ['info'])



    def addevent(self, title, start, end, **args):
        event_dict = {"title": title, "start": start, "end": end, **args}
        self._props['options']['events'].append(event_dict)
        super().update()
        self.run_method('update_calendar')

    def remove_event(self, title, start, end, **args):

        for event in self._props['options']['events']:
            if event['title'] == title and event['start'] == start and event['end'] == end:
                self._props['options']['events'].remove(event)
                break

        super().update()
        self.run_method('update_calendar')
    def get_events(self):
        return self._props['options']['events']
        
