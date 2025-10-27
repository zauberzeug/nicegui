import asyncio

from nicegui import ui

from . import doc


@doc.demo(ui.xterm)
def main_demo() -> None:
    terminal = ui.xterm({'cols': 30, 'rows': 9})
    ui.timer(0, lambda: terminal.write('Hello NiceGUI!'), once=True)


@doc.demo('Using ANSI escape codes', '''
    Xterm can parse ANSI escape codes to style text in the terminal.
    Use the `writeln` method instead of `write` to automatically add a newline and carriage return after the text.
''')
def ansi_escape_codes():
    terminal = ui.xterm({'cols': 30, 'rows': 9})
    ui.button('Add normal text', on_click=lambda: terminal.writeln('This is normal text.'))
    ui.button('Add blue text', on_click=lambda: terminal.writeln('\x1b[34mThis text is blue!\x1b[0m'))
    ui.button('Add bold text', on_click=lambda: terminal.writeln('\x1b[1mThis text is bold!\x1b[0m'))


@doc.demo('Subscribing to events', '''
    Xterm emits a "data" event when you type or paste text into the terminal.
    Normally, you would pass this data to a pty or similar backend to process it
    (see the [Xterm example](https://github.com/zauberzeug/nicegui/blob/main/examples/xterm/main.py)).
    However, you can also connect this event to the terminal's `write` method to see the data in the terminal.
    Notice that this demo replaces some characters, which would otherwise be done by the pty (newline and backspace).

    You can also handle the "bell" event, e.g. to play a sound when the terminal's bell is triggered
    (e.g. by pressing `Ctrl-G`).
    This demo shows a notification instead.
''')
def subscribing_to_events():
    terminal = ui.xterm({'cols': 30, 'rows': 9})
    terminal.on_data(lambda e: terminal.write(e.data.replace('\r', '\n\r').replace('\x7f', '\x1b[0D\x1b[0K')))
    terminal.on_bell(lambda: ui.notify('🔔'))


@doc.demo('Auto-resizing the terminal', '''
    You can use the `fit` method to resize the terminal,
    so that its number of rows and columns match the size of its container.
    Note that you might also need to resize the backing pty to match the new size of the terminal,
    which you can do by subscribing to the terminal's `resize` event.
    Also note that the native `pty` module does not support resizing.
''')
def resizing():
    with ui.card().classes('size-60 resize overflow-auto'):
        terminal = ui.xterm().classes('size-full')
        ui.element('q-resize-observer').on('resize', terminal.fit)

    label = ui.label()
    terminal.on('resize', lambda e: label.set_text(f'Size: {e.args["cols"]}x{e.args["rows"]}'))


@doc.demo('Showing output of a subprocess', '''
    You can connect the output of a subprocess to the terminal.
    Note that `subprocess.PIPE` buffers the output in `StreamReader` objects in memory.
    If you want your subprocess to behave like it is running in a terminal, you might need to use a pty.
    The `convertEol` parameter automatically converts line feeds (`\\n`) to carriage return + line feed (`\\r\\n`),
    which ensures proper line breaks when displaying subprocess output.
''')
def connecting_to_subprocess():
    async def run_subprocess():
        button.disable()
        process = await asyncio.create_subprocess_exec(
            'python3', '-u', '-c',
            (
                'import time\n'
                'for i in range(5):\n'
                '    print(f"Step {i+1}/5: Processing...")\n'
                '    time.sleep(0.5)\n'
                'print("\\x1b[32m✓ All steps completed!\\x1b[0m")'
            ),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def write_to_terminal(stream: asyncio.StreamReader) -> None:
            while chunk := await stream.read(128):
                terminal.write(chunk)

        await asyncio.gather(
            write_to_terminal(process.stdout),
            write_to_terminal(process.stderr),
            process.wait(),
        )
        button.enable()

    terminal = ui.xterm({'cols': 30, 'rows': 9, 'convertEol': True})
    button = ui.button('Run subprocess', on_click=run_subprocess)


doc.reference(ui.xterm)
