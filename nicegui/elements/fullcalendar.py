
from typing import List, Dict
from ..element import Element

class FullCalendar(Element, component="fullcalendar.js", exposed_libraries=["https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/main.min.css", "https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js"]):
    def __init__(self, events_data: List[Dict], element_id: str = 'full-calendar') -> None:
        super().__init__('fullcalendar.js')
        self._props['eventsData'] = events_data
        self._props['elementId'] = element_id