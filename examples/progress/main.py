#!/usr/bin/env python3
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, Queue

from nicegui import app, ui

pool = ProcessPoolExecutor()


def heavy_computation(q: Queue):
    '''Some heavy computation that updates the progress bar through the queue.'''
    n = 50
    for i in range(n):
        # Perform some heavy computation
        time.sleep(0.1)

        # Update the progress bar through the queue
        q.put_nowait(i / n)
    return 'Done!'


@ui.page('/')
def main_page():

    async def start_computation():
        progressbar.visible = True
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(pool, heavy_computation, queue)
        ui.notify(result)
        progressbar.visible = False

    # Create a queue to communicate with the heavy computation process
    queue = Manager().Queue()
    # Update the progress bar on the main process
    ui.timer(0.1, callback=lambda: progressbar.set_value(queue.get() if not queue.empty() else progressbar.value))

    # Create the UI
    ui.button('compute', on_click=start_computation)
    progressbar = ui.linear_progress(value=0).props('instant-feedback')
    progressbar.visible = False


# stop the pool when the app is closed; will not cancel any running tasks
app.on_shutdown(lambda: pool.shutdown(cancel_futures=True))

ui.run()
