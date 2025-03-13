#!/usr/bin/env python3
import time

from nicegui import run, ui  # sets NICEGUI_HOST environment variable; if NICEGUI_HOST is set, imports a hull


# unpickling does not import NiceGUI because `run` is implemented outside of nicegui module
def simulate_work():
    print('Working...')
    time.sleep(1.0)
    print('Done.')


# TODO: NiceGUI main_guard to selectively run user code?
# if main_guard:
#     print('Doing heavy work...')

ui.button('Work', on_click=lambda: run.cpu_bound(simulate_work))

ui.run(reload=False)  # does nothing if NICEGUI_HOST is set
# ui.run()  # TODO
