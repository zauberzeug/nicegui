#!/usr/bin/env python3
import time
from multiprocessing import Manager, Queue

from nicegui import run, ui


def heavy_computation(q: Queue) -> str:
    """
    Run some heavy computation that updates the progress bar through the queue.

    Parameters:
    - q (Queue): A queue object used to update the progress bar.

    Returns:
    - str: A message indicating that the computation is done.

    Usage:
    1. Create a Queue object and pass it as an argument to this function.
    2. Start a separate thread to run this function.
    3. The function will perform heavy computation in a loop and update the progress bar through the queue.
    4. Once the computation is complete, the function will return a message indicating that it's done.
    """

    n = 50
    for i in range(n):
        # Perform some heavy computation
        time.sleep(0.1)

        # Update the progress bar through the queue
        q.put_nowait(i / n)
    return 'Done!'


@ui.page('/')
def main_page():
    """
    This function represents the main page of the application.
    It contains the logic for starting a heavy computation process and updating a progress bar.

    Usage:
    - Call this function to create the main page of the application.
    - Clicking the 'compute' button will start the heavy computation process.
    - The progress bar will be updated as the computation progresses.
    - The result of the computation will be displayed in a notification.

    Example:
    >>> main_page()
    """

    async def start_computation():
        """
        Start the heavy computation process.

        This function is called when the 'compute' button is clicked.
        It sets the visibility of the progress bar, runs the heavy computation,
        displays the result in a notification, and hides the progress bar.

        Usage:
        - This function is automatically called when the 'compute' button is clicked.

        Example:
        >>> await start_computation()
        """
        progressbar.visible = True
        result = await run.cpu_bound(heavy_computation, queue)
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


ui.run()
