from typing import Any, Callable, Dict, List, Optional

from ..element import Element
from ..events import GenericEventArguments, handle_event




class FullCalendar(Element, component='fullcalendar.js', libraries=['lib/fullcalendar/index.global.min.js']):
    def __init__(self, options: Dict[str, Any], on_click: Optional[Callable] = None) -> None:
        super().__init__()
        self._props['options'] = options
        
        if on_click:
            def handle_on_click(e: GenericEventArguments):
                # print(e)
                handle_event(on_click, e)

            self.on("click", handle_on_click, ['info'])

    def updater(self, event) -> None:
        super().update()
        print("Attempting to update!")
        self.run_method('update_calendar', event)

    def updatecal(self, options: Dict[str, Any]) -> None:
        # Implement your logic here to update the calendar with the new options
        print("Updating calendar with options:", options)
        # You might want to update the FullCalendar instance with the new options
        self._props['options'] = options
        self.updater(None)
    

    def addevent(self, event):
        self._props['eventToAdd'] = event
        self._props['options']['events'].append(event)
        # super().update()
        print("Attempting to add an event", event)
        # self.run_method('add_event', event)
        self.updater(event)