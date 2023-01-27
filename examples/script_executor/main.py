#!/usr/bin/env python3

import asyncio
import os
import shlex

from nicegui import background_tasks, ui
from nicegui.element import Element


async def run_command(command: str) -> None:
    dialog.open()
    result.content = ''
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        cwd=os.path.dirname(os.path.abspath(__file__)))
    content = ''
    while True:
        new = await process.stdout.read(4096)
        if not new:
            break
        content += new.decode()
        result.content = f'```\n{content}\n```'

with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

commands = ['python3 hello.py', 'python3 hello.py NiceGUI', 'python3 slow.py']
with ui.row():
    for command in commands:
        ui.button(command, on_click=lambda _, c=command: background_tasks.create(run_command(c))).props('no-caps')


ui.run()
