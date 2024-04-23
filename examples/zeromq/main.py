from datetime import datetime

import zmq
import zmq.asyncio

from nicegui import app, run, ui

# Create a ZMQ context
context = zmq.asyncio.Context()

# Create a ZMQ socket and connect it to the server
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5555")

poller = zmq.asyncio.Poller()
poller.register(socket, zmq.POLLIN)


async def read_loop() -> None:
    while not app.is_stopped:
        events = await poller.poll()
        if socket in dict(events):
            print("received", events)
            message = await socket.recv_multipart()
            print("Binary message: ", message)

            # Convert the message values to floats
            numbers = [float(x) for x in message]

            print("Float message: ", numbers)

            now = datetime.now()
            line_plot.push([now], [[numbers[0]]])

line_plot = ui.line_plot(n=1, limit=100, figsize=(10, 4), close=False)

app.on_startup(read_loop)

ui.run()
