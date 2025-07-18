#!/usr/bin/env python3
"""Example for connecting a `Xterm` element with a `Bash` process running in a pty.

WARNING: This example gives the clients full access to the server through Bash. Use with caution!
"""

import asyncio
import logging
import os
import pty
import signal

from nicegui import context, ui
from nicegui.events import XtermDataEventArguments
from nicegui.logging import log


# We create the terminals in a `ui.page`, so that each client gets its own terminal
@ui.page('/')
def _page():
    # We now create the terminal (front-end) element for the client
    client = context.client
    ui.label(f'Terminal ({client.id})').style('font-weight: bold;')
    terminal = ui.xterm()

    # Add bell sound
    bell_sound = ui.audio('https://www.soundjay.com/buttons/beep-07a.mp3', controls=False)
    terminal.on_bell(lambda _: bell_sound.play())

    async def run_bash():
        # At this point, we need to create a new pseudo-terminal (pty) fork of the process
        pty_pid, pty_fd = pty.fork()
        if pty_pid == pty.CHILD:
            # The child process of the fork gets replaced with 'bash'
            os.execv('/bin/bash', ('bash',))
        log.info('Terminal opened: %s', client.id)

        def pty_to_terminal():
            try:
                data = os.read(pty_fd, 1024)
            except OSError:
                # There was an error reading the pty; probably bash was exited. Let's stop reading from it.
                log.info('Stopping reading from pty: %s', client.id)
                loop.remove_reader(pty_fd)
            else:
                terminal.write(data)

        def terminal_to_pty(event: XtermDataEventArguments):
            try:
                os.write(pty_fd, event.data.encode('utf-8'))
            except OSError:
                # There was an error writing to the pty; probably bash was exited. Nothing to do.
                pass

        # Now we can connect the pty to the terminal
        loop = asyncio.get_event_loop()
        loop.add_reader(pty_fd, pty_to_terminal)
        terminal.on_data(terminal_to_pty)

        def kill_bash():
            os.close(pty_fd)
            os.kill(pty_pid, signal.SIGKILL)
            log.info('Terminal closed: %s', client.id)

        # Make sure to kill the bash process when the client disconnects
        client.on_disconnect(kill_bash)
        await client.disconnected()

    client.safe_invoke(run_bash())


if __name__ in {'__main__', '__mp_main__'}:
    logging.basicConfig(level=logging.INFO)
    ui.run()
