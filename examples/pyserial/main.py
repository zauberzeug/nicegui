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
    """
    Asynchronous function that continuously reads lines from a serial port and logs them.

    This function runs in a loop until the `app.is_stopped` flag is set to True.
    It reads a line from the `port` using the `readline` method and decodes it.
    If a line is read, it is pushed to the log.

    Note:
        - This function should be called within an event loop.
        - The `port` variable should be an instance of a serial port object.

    Example usage:
        # Create a serial port object
        port = serial.Serial('/dev/ttyUSB0', baudrate=9600)

        # Start the read loop
        await read_loop()

    Returns:
        None
    """
    while not app.is_stopped:
        line = await run.io_bound(port.readline)
        if line:
            log.push(line.decode())

app.on_startup(read_loop)

ui.run()
