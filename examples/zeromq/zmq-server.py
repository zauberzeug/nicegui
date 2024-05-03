#!/usr/bin/env python3
import asyncio
import random

import zmq
import zmq.asyncio

context = zmq.asyncio.Context()
socket = context.socket(zmq.PUSH)
socket.bind('tcp://localhost:5555')


async def send_loop():
    while True:
        number = random.randint(0, 100)
        print(f'Sending number {number}')
        await socket.send(str(number).encode('ascii'))
        await asyncio.sleep(0.1)


asyncio.run(send_loop())
