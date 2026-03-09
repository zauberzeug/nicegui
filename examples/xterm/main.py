#!/usr/bin/env python3
"""Example for connecting a `Xterm` element with a `Bash` process running in a pty.

WARNING: This example gives the clients full access to the server through Bash. Use with caution!
"""
import fcntl
import os
import pty
import signal
import struct
import termios
from functools import partial

from nicegui import core, events, ui


@ui.page('/')
def _page():
    initial_cols = 100
    initial_rows = 20
    terminal = ui.xterm({'cols': initial_cols, 'rows': initial_rows})
    ui.button('Fill', on_click=lambda: terminal.classes('size-full'))
    ui.button('Fit', on_click=terminal.fit)

    pty_pid, pty_fd = pty.fork()  # create a new pseudo-terminal (pty) fork of the process
    if pty_pid == pty.CHILD:
        os.execv('/bin/bash', ('bash',))  # child process of the fork gets replaced with "bash"
    print('Terminal opened')

    # sends to the pty the control code to inform it of the current terminal size
    def set_terminal_size(cols: int, rows: int):
        fcntl.ioctl(pty_fd, termios.TIOCSWINSZ, struct.pack('HHHH', rows, cols, 0, 0))
    # you can check it by running this in the xterm terminal:
    # python -c "import os; print(os.get_terminal_size())"
    set_terminal_size(initial_cols, initial_rows)

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

    @terminal.on_resize
    def resize_terminal(event: events.XtermResizeEventArguments):
        print(f'A resize happened: {event=}')
        set_terminal_size(event.cols, event.rows)

    @ui.context.client.on_delete
    def kill_bash():
        os.close(pty_fd)
        os.kill(pty_pid, signal.SIGKILL)
        print('Terminal closed')


ui.run()
