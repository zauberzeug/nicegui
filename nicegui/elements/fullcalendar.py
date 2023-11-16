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



    def addevent(self, title, start, end, **args):
        event_dict = {"title": title, "start": start, "end": end, **args}
        self._props['options']['events'].append(event_dict)
        super().update()
        self.run_method('update_calendar')
        super().update()

    def remove_event(self, title, start, end, **args):
        index_to_remove = None
        for i, event in enumerate(self._props['options']['events']):
            if (
                event["title"] == title
                and event["start"] == start
                and event["end"] == end
                and all(event[key] == args[key] for key in args)
            ):
                index_to_remove = i
                break

        # Remove the event if found
        if index_to_remove is not None:
            del self._props['options']['events'][index_to_remove]
        super().update()
        self.run_method('update_calendar')
        
