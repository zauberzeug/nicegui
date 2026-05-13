from datetime import datetime
from typing import cast

from nicegui import Event, app, binding


class Lightbulb:
    """A controllable lightbulb with bindable properties and events."""
    power = binding.BindableProperty(
        lambda sender, value: cast(Lightbulb, sender)._handle_power(value),  # pylint: disable=protected-access
    )
    brightness = binding.BindableProperty(
        lambda sender, value: cast(Lightbulb, sender)._handle_brightness(value),  # pylint: disable=protected-access
    )

    def __init__(self) -> None:
        self.power = False
        self.brightness = 50
        self._heartbeat_timer = app.timer(10, self._heartbeat, active=False)

        self.power_changed = Event[bool]()
        '''The power state changed (argument: new power state).'''

        self.brightness_changed = Event[int]()
        '''The brightness changed (argument: new brightness).'''

        self.log_message = Event[str]()
        '''A log message to be displayed in the UI (argument: message).'''

    def _handle_power(self, value: bool) -> None:
        self._heartbeat_timer.active = value
        self._log(f'Lightbulb is now {"ON" if value else "OFF"}')
        self.power_changed.emit(value)

    def _handle_brightness(self, value: int) -> None:
        value = max(0, min(100, value))
        self._log(f'Brightness set to {value}%')
        self.brightness_changed.emit(value)

    def _heartbeat(self) -> None:
        self._log(f'Status: ONLINE | Brightness: {self.brightness}%')

    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_message.emit(f'[{timestamp}] {message}')
