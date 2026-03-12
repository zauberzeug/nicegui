#!/usr/bin/env python3
"""Example for connecting a `Xterm` element with a `Bash` process running in a pty.

WARNING: This example gives the clients full access to the server through Bash. Use with caution!
"""
import os
import pty
import signal
from functools import partial

from nicegui import core, events, ui


@ui.page('/')
def _page():
    terminal = ui.xterm()

    pty_pid, pty_fd = pty.fork()  # create a new pseudo-terminal (pty) fork of the process
    if pty_pid == pty.CHILD:
        os.execv('/bin/bash', ('bash',))  # child process of the fork gets replaced with "bash"
    print('Terminal opened')

    @partial(core.loop.add_reader, pty_fd)
    def pty_to_terminal():
        try:
            data = os.read(pty_fd, 1024)
        except OSError:
            print('Stopping reading from pty')  # error reading the pty; probably bash was exited
            core.loop.remove_reader(pty_fd)
        else:
            terminal.write(data)

    @terminal.on_data
    def terminal_to_pty(event: events.XtermDataEventArguments):
        try:
            os.write(pty_fd, event.data.encode('utf-8'))
        except OSError:
            pass  # error writing to the pty; probably bash was exited

    @ui.context.client.on_delete
    def kill_bash():
        os.close(pty_fd)
        os.kill(pty_pid, signal.SIGKILL)
        print('Terminal closed')


ui.run()
