#!/usr/bin/env python3
import random
from typing import Optional, cast

from typing_extensions import Self

from nicegui import ui
from nicegui.binding import BindableProperty, bind_from


class colorful_label(ui.label):
    """A label with a bindable background color."""

    # This class variable defines what happens when the background property changes.
    background = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_background_change(value))

    def __init__(self, text: str = '') -> None:
        super().__init__(text)
        self.background: Optional[str] = None  # initialize the background property

    def _handle_background_change(self, bg_class: str) -> None:
        """Update the classes of the label when the background property changes."""
        self._classes = [c for c in self._classes if not c.startswith('bg-')]
        self._classes.append(bg_class)
        self.update()


temperatures = {'Berlin': 5, 'New York': 15, 'Tokio': 25}
ui.button(icon='refresh', on_click=lambda: temperatures.update({city: random.randint(0, 30) for city in temperatures}))


for city in temperatures:
    label = colorful_label().classes('w-48 text-center') \
        .bind_text_from(temperatures, city, backward=lambda t, city=city: f'{city} ({t}°C)')
    # Bind background color from temperature.
    # There is also a bind_to method which would propagate changes from the label to the temperatures dictionary
    # and a bind method which would propagate changes both ways.
    bind_from(self_obj=label, self_name='background',
              other_obj=temperatures, other_name=city,
              backward=lambda t: 'bg-green' if t < 10 else 'bg-yellow' if t < 20 else 'bg-orange')

ui.run()
