#!/usr/bin/env python3
from lightbulb import Lightbulb

from nicegui import ui

lightbulb = Lightbulb()


def root() -> None:
    ui.markdown('### Lightbulb Control')
    ui.checkbox('Power').bind_value(lightbulb, 'power').props('checked-icon=lightbulb unchecked-icon=sym_o_light_off')
    ui.slider(min=0, max=100).bind_value(lightbulb, 'brightness').classes('w-60').bind_enabled_from(lightbulb, 'power')

    ui.markdown('### Device Log')
    log = ui.log()
    lightbulb.log_message.subscribe(log.push)

    lightbulb.power_changed.subscribe(lambda value: ui.notify(f'Power {"ON" if value else "OFF"}'))


ui.run(root)
