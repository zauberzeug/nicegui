import uuid

from nicegui.element import Element


class Timeline(Element, component='timeline.js'):

    def __init__(self, initial_items: list = None, timelinecolor: str = "secondary") -> None:
        super().__init__()
        if initial_items:
            self._props['initialItems'] = initial_items
            self._props['timelinecolor'] = timelinecolor

    """Timeline

    :param initialItems: Items of the timeline. Should be an Array of dictionarys and contain the id, title, subtitle, icon, body
    :param timelinecolor: Color of the Icons. Should be an quasar color

    See `here <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events>`_
    for a list of events you can subscribe to using the generic event subscription `on()`.
    """

    def _generate_id(self):
        """Generate a unique ID for each timeline item."""
        return str(uuid.uuid4())

# Example Usage:
# timeline = Timeline()
# timeline.add_item(heading="Timeline Heading", title="Event Title", subtitle="Date", body="Description")
