#!/usr/bin/env python3
from datetime import datetime

from nicegui import app, ui
from nicegui.event import Event
from nicegui.timer import Timer


class Lightbulb:
    """A controllable lightbulb with events."""

    def __init__(self) -> None:
        self._power: bool = False
        self._brightness: int = 50
        self._heartbeat_timer: Timer | None = None

        self.power_changed = Event[bool]()
        self.brightness_changed = Event[int]()
        self.log_message = Event[str]()

    def _log(self, message: str) -> None:
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_message.emit(f'[{timestamp}] {message}')

    def _heartbeat(self) -> None:
        self._log(f'Status: ONLINE | Brightness: {self._brightness}%')

    @property
    def power(self) -> bool:
        return self._power

    @power.setter
    def power(self, value: bool) -> None:
        if value != self._power:
            self._power = value
            if value:
                self._log('Lightbulb is now ON')
                self._heartbeat_timer = app.timer(10, self._heartbeat)
            else:
                self._log('Lightbulb is now OFF')
                if self._heartbeat_timer:
                    self._heartbeat_timer.cancel()
                    self._heartbeat_timer = None
            self.power_changed.emit(value)

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        value = max(0, min(100, value))
        if value != self._brightness:
            self._brightness = value
            self._log(f'Brightness set to {value}%')
            self.brightness_changed.emit(value)


lightbulb = Lightbulb()


@ui.page('/')
def main() -> None:

    def toggle_power() -> None:
        lightbulb.power = not lightbulb.power

    def update_power_ui(is_on: bool) -> None:
        power_icon.classes(replace='text-yellow' if is_on else 'text-grey')
        power_label.set_text('ON' if is_on else 'OFF')
        brightness_slider.set_enabled(is_on)

    def update_brightness_ui(value: int) -> None:
        brightness_slider.set_value(value)
        brightness_label.set_text(f'{value}%')

    lightbulb.power_changed.subscribe(update_power_ui)
    lightbulb.brightness_changed.subscribe(update_brightness_ui)

    ui.label('Lightbulb Control').classes('text-h4 q-mb-md')

    with ui.row().classes('items-center gap-2'):
        ui.label('Power:')
        power_icon = ui.icon('lightbulb', size='lg').classes('cursor-pointer') \
            .on('click', toggle_power)
        power_label = ui.label()

    with ui.row().classes('items-center gap-4 q-mt-md w-full'):
        ui.label('Brightness:').classes('w-24')
        brightness_slider = ui.slider(min=0, max=100, value=lightbulb.brightness).classes('w-full') \
            .on('update:model-value', lambda e: setattr(lightbulb, 'brightness', int(e.args)))
        brightness_label = ui.label()

    ui.label('Device Log').classes('text-h6 q-mt-lg q-mb-sm')
    log = ui.log().classes('w-full h-48')

    lightbulb.log_message.subscribe(log.push)

    update_power_ui(lightbulb.power)
    update_brightness_ui(lightbulb.brightness)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
