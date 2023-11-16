from typing import Dict, List, Optional, Callable

from ..element import Element
from ..events import GenericEventArguments, handle_event

class FullCalendar(Element, component='fullcalendar.js', libraries=['lib/fullcalendar/index.global.min.js']):
    def __init__(self, events_data: List[Dict], on_click: Optional[Callable] = None) -> None:
        super().__init__()
        self._props['eventsData'] = events_data
        if on_click:
            def handle_on_click(e: GenericEventArguments):
                print(e)
                handle_event(on_click, e)
        
            self.on("click", handle_on_click, ['click'])


    def on_event_clicked(self, event_info):
        # Implement your logic to handle the clicked event in Python
        print("Event clicked in Python:", event_info)
