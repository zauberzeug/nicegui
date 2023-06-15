#!/usr/bin/env python3
import asyncio
import os.path
import platform
import shlex

from nicegui import ui


async def run_command(command: str) -> None:
    """Run a command in the background and display the output in the pre-created dialog."""
    dialog.open()
    result.content = ''
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    # NOTE we need to read the output in chunks, otherwise the process will block
    output = ''
    while True:
        new = await process.stdout.read(4096)
        if not new:
            break
        output += new.decode()
        # NOTE the content of the markdown element is replaced every time we have new output
        result.content = f'```\n{output}\n```'

with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

commands = ['python3 hello.py', 'python3 hello.py NiceGUI', 'python3 slow.py']
with ui.row():
    for command in commands:
        ui.button(command, on_click=lambda command=command: run_command(command)).props('no-caps')


# NOTE on windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(reload=platform.system() != "Windows")
