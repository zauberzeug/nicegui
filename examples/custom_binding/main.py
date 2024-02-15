#!/usr/bin/env python3
import random
from typing import Optional, cast

from typing_extensions import Self

from nicegui import ui
from nicegui.binding import BindableProperty, bind_from


class colorful_label(ui.label):
    """A label with a bindable background color.

    This class represents a label widget that can have a bindable background color.
    It inherits from the `ui.label` class.

    Attributes:
        background (BindableProperty): A class variable that defines what happens when the background property changes.

    Methods:
        __init__(self, text: str = ''): Initializes the colorful_label object.
        _handle_background_change(self, bg_class: str): Updates the classes of the label when the background property changes.

    Usage:
        label = colorful_label("Hello, World!")
        label.background = "bg-red"  # Set the background color to red
    """

    background = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_background_change(value))

    def __init__(self, text: str = '') -> None:
        """Initialize the colorful_label object.

        Args:
            text (str): The text to be displayed on the label. Defaults to an empty string.
        """
        super().__init__(text)
        self.background: Optional[str] = None  # initialize the background property

    def _handle_background_change(self, bg_class: str) -> None:
        """Update the classes of the label when the background property changes.

        This method is called when the background property of the label is changed.
        It updates the classes of the label by removing any existing background classes
        and adding the new background class specified.

        Args:
            bg_class (str): The new background class to be applied to the label.
        """
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
