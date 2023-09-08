#!/usr/bin/env python3

import random

from nicegui import ui
from nicegui.binding import BindableProperty, bind_from


class colorful_label(ui.label):
    """A label with a bindable background color."""

    # this class variable defines what happens when the background property changes
    background = BindableProperty(on_change=lambda sender, bg: sender.on_background_change(bg))

    def __init__(self, text: str):
        super().__init__(text)
        self.background = None  # initialize the background property

    def on_background_change(self, bg: str) -> None:
        """Update the classes of the label when the background property changes."""
        self._classes = [c for c in self._classes if not c.startswith('bg-')]
        self._classes.append(bg)
        self.update()


def shuffle():
    for key in data:
        data[key] = random.choice([True, False])


ui.button('shuffle', on_click=shuffle)
data = {}
for k in 'abcde':
    data[k] = random.choice([True, False])
    label = colorful_label(k.upper()).classes('w-48 text-center')
    # binding from the data to the label
    # there is also a bind_to method which would propagate changes from the label to the data
    # and a bind method which would propagate changes both ways
    bind_from(label, 'background', data, k, backward=lambda x: 'bg-green' if x else 'bg-red')

ui.run()
