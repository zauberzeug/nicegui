from nicegui import ui

from ..tools import load_demo

name = 'controls'
title = 'Controls'


def intro() -> None:
    ...


def content() -> None:
    load_demo(ui.button)
    load_demo(ui.badge)
    load_demo(ui.toggle)
    load_demo(ui.radio)
    load_demo(ui.select)
    load_demo(ui.checkbox)
    load_demo(ui.switch)
    load_demo(ui.slider)
    load_demo(ui.joystick)
    load_demo(ui.input)
    load_demo(ui.textarea)
    load_demo(ui.number)
    load_demo(ui.knob)
    load_demo(ui.color_input)
    load_demo(ui.color_picker)
    load_demo(ui.date)
    load_demo(ui.time)
    load_demo(ui.upload)
