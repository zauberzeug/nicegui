import asyncio
import random

import zmq
import zmq.asyncio

context = zmq.asyncio.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://localhost:5555")


async def send_loop():
    while True:
        # Generate a random number.
        rand_int = random.randint(0, 100)
        # Send an integer to the client.
        await socket.send_multipart([str(rand_int).encode('ascii')])

        print("Sent Number: ", rand_int)
        await asyncio.sleep(0.1)


asyncio.run(
    asyncio.wait(
        [
            send_loop(),
        ]
    )
)
