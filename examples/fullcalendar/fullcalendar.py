from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nicegui import events, ui


@dataclass
class FetchInfoArguments(events.EventArguments):
    """Arguments passed to the ``on_fetch_events`` callback.

    Contains the date range FullCalendar is requesting events for, plus a
    ``request_id`` that must be passed back via :meth:`response` or :meth:`failure`
    so the result is delivered to the correct pending callback on the client.
    """
    request_id: int
    start: str
    end: str
    start_value: int
    end_value: int
    time_zone: str
    sender: Any = None

    def response(self, events_list: list[dict]) -> None:
        """Send the fetched events back to the calendar."""
        self.sender.run_method('on_events_fetched', self.request_id, events_list)

    def failure(self, error: str | None = None) -> None:
        """Notify the calendar that the fetch failed."""
        self.sender.run_method('on_events_failed', self.request_id, error)


class FullCalendar(ui.element, component='fullcalendar.js'):

    def __init__(
        self,
        options: dict[str, Any],
        on_click: Callable | None = None,
        on_fetch_events: Callable | None = None,
    ) -> None:
        """FullCalendar

        An element that integrates the FullCalendar library (https://fullcalendar.io/) to create an interactive calendar display.
        For an example of the FullCalendar library with plugins see https://github.com/dorel14/NiceGui-FullCalendar_more_Options

        :param options: dictionary of FullCalendar properties for customization, such as "initialView", "slotMinTime", "slotMaxTime", "allDaySlot", "timeZone", "height", and "events".
        :param on_click: callback that is called when a calendar event is clicked.
        :param on_fetch_events: callback that is called when FullCalendar requests events for a date range.
            The callback receives a :class:`FetchInfoArguments` and must call ``response(events)``
            (or ``failure(error)``) on the received object to deliver the events back to the calendar.
            The ``options`` dict must contain ``"events": callable`` to activate this feature.
        """

        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib')
        options = dict(options)
        self._events_function = None
        if callable(options.get('events')):
            self._events_function = options.pop('events')
            options['events'] = '__fetch__'
        self._props['options'] = options
        self._update_method = 'update_calendar'

        if on_click:
            self.on('click', lambda e: events.handle_event(on_click, e))

        if on_fetch_events:
            def _on_fetch(e: events.GenericEventArguments) -> None:
                info = FetchInfoArguments(
                    request_id=e.args['request_id'],
                    start=e.args['start'],
                    end=e.args['end'],
                    start_value=e.args['start_value'],
                    end_value=e.args['end_value'],
                    time_zone=e.args['time_zone'],
                    sender=self,
                )
                events.handle_event(on_fetch_events, info)
            self.on('fetch-events', _on_fetch)

    def add_event(self, title: str, start: str, end: str, **kwargs) -> None:
        """Add an event to the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        event_dict = {'title': title, 'start': start, 'end': end, **kwargs}
        self._props['options']['events'].append(event_dict)

    def remove_event(self, title: str, start: str, end: str) -> None:
        """Remove an event from the calendar.

        :param title: title of the event
        :param start: start time of the event
        :param end: end time of the event
        """
        for event in self._props['options']['events']:
            if event['title'] == title and event['start'] == start and event['end'] == end:
                self._props['options']['events'].remove(event)
                break

    @property
    def events(self) -> list[dict]:
        """List of events currently displayed in the calendar."""
        return self._props['options']['events']

