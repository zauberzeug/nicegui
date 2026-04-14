#!/usr/bin/env python3
"""Example for connecting a `Xterm` element with a process running in a pty.

Pass a command as argument to run something other than bash, e.g.::

    python main.py top
    python main.py "python3 -m textual_paint"

WARNING: This example gives the clients full access to the server through a shell process. Use with caution!
"""
import fcntl
import os
import pty
import shlex
import signal
import struct
import sys
import termios
from functools import partial

from nicegui import core, events, ui

command = shlex.split(sys.argv[1]) if len(sys.argv) > 1 else ['/bin/bash']


@ui.page('/')
async def _page():
    ui.query('.nicegui-content').classes('p-0')  # remove padding so the terminal can fill the viewport
    terminal = ui.xterm().classes('w-screen h-screen')
    ui.element('q-resize-observer').on('resize', terminal.fit)

    pty_pid = 0
    pty_fd = -1

    @terminal.on_data
    def terminal_to_pty(event: events.XtermDataEventArguments):
        try:
            os.write(pty_fd, event.data.encode('utf-8'))
        except OSError:
            pass  # error writing to the pty; probably the process was exited

    @terminal.on_resize
    def resize_terminal(event: events.XtermResizeEventArguments):
        if pty_fd < 0:
            return
        fcntl.ioctl(pty_fd, termios.TIOCSWINSZ, struct.pack('HHHH', event.rows, event.cols, 0, 0))

    @ui.context.client.on_delete
    def kill_process():
        if pty_fd >= 0:
            os.close(pty_fd)
            os.kill(pty_pid, signal.SIGKILL)
            print('Terminal closed')

    await ui.context.client.connected()
    pty_pid, pty_fd = pty.fork()  # create a new pseudo-terminal (pty) fork of the process
    if pty_pid == pty.CHILD:
        os.environ['TERM'] = 'xterm-256color'
        os.environ['COLORTERM'] = 'truecolor'
        os.execvp(command[0], command)  # replace the child process with the requested command
    print('Terminal opened')

    @partial(core.loop.add_reader, pty_fd)
    def pty_to_terminal():
        try:
            data = os.read(pty_fd, 1024)
        except OSError:
            print('Stopping reading from pty')  # error reading the pty; probably the process was exited
            core.loop.remove_reader(pty_fd)
        else:
            if not terminal.is_deleted:
                terminal.write(data)


ui.run()
