


class CalendarEvent():
    def __init__(self) -> None:
        self.events = []
    def add_event(self, title, start, end, **args):
        event_dict = {"title": title, "start": start, "end": end, **args}
        self.events.append(event_dict)
    def get_events(self):
        return self.events

    def remove_event(self, title, start, end, **args):
        index_to_remove = None
        for i, event in enumerate(self.events):
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
            del self.events[index_to_remove]
