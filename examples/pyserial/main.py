#!/usr/bin/env python3
import serial

from nicegui import app, run, ui

port = serial.Serial('/dev/tty.SLAB_USBtoUART', baudrate=115200, timeout=0.1)

ui.input('Send command').on('keydown.enter', lambda e: (
    port.write(f'{e.sender.value}\n'.encode()),
    e.sender.set_value(''),
))
log = ui.log()


async def read_loop() -> None:
    while not app.is_stopped:
        line = await run.io_bound(port.readline)
        if line:
            log.push(line.decode())

app.on_startup(read_loop)

ui.run()
