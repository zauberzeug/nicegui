import asyncio

from nicegui import ui

from . import doc


@doc.demo(ui.xterm)
def main_demo() -> None:
    terminal = ui.xterm({'cols': 30, 'rows': 9})
    ui.timer(0.1, lambda: terminal.write('Hello NiceGUI!'), once=True)


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
    Xterm emits a `data` event when you type or paste text into the terminal.
    Normally, you would pass this data to a pty or similar backend to process it (see the
    [Xterm example](https://github.com/zauberzeug/nicegui/blob/main/examples/xterm/main.py)).
    However, you can also connect this event to the terminal's `write` method to see the data in the terminal.
    Notice that this demo replaces some characters, which would otherwise be done by the pty.
    You can also connect an audio element to the `bell` event to play a sound when the terminal's bell is triggered
    (e.g. by pressing `Ctrl-G`).
''')
def on_data_event():
    terminal = ui.xterm({'cols': 30, 'rows': 9})
    terminal.on_data(lambda event: terminal.write(event.data.replace('\r', '\n\r').replace('\x7f', '\x1b[0D\x1b[0K')))
    terminal.on_data(lambda e: print(e.data.encode()))

    bell_sound = ui.audio('https://www.soundjay.com/buttons/beep-07a.mp3', controls=False)
    terminal.on_bell(lambda _: bell_sound.play())


@doc.demo('Auto-resizing the terminal', '''
    You can use the `fit` method to resize the terminal, so that its number of rows and columns match the size of its
    container.
    Note that you might also need to resize the backing pty to match the new size of the terminal, which you can do by
    subscribing to the terminal's `resize` event. Also note that the native `pty` module does not support resizing.
''')
def resizing():
    with ui.card().style('resize:both; overflow: auto; width: 300px; height: 200px;'):
        resize_observer = ui.element('q-resize-observer')
        terminal = ui.xterm().classes('size-full')

    size_label = ui.label('Terminal size:')
    resize_observer.on('resize', terminal.fit)
    terminal.on('resize', lambda e: size_label.set_text(f'Terminal size: {e.args["cols"]}x{e.args["rows"]}'))


@doc.demo('Showing output of a subprocess', '''
    You can connect the output of a subprocess to the terminal.
    Note that `subprocess.PIPE` buffers the output in `StreamReader` objects in memory.
    If you want your subprocess to behave like it's running in a terminal, you might need to use a pty.
''')
def connecting_to_subprocess():
    async def run_subprocess():
        button.disable()
        process = await asyncio.create_subprocess_exec(
            'python3', '-c',
            (
                'import time; [print(f"\\r[{\'#\' * i}{\' \' * (10 - i)}] {i * 10}%", end="", flush=True) or '
                'time.sleep(0.5) for i in range(11)]; print("\x1b[32m  Done!\x1b[0m")'
            ),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def write_to_terminal(stream: asyncio.StreamReader) -> None:
            while chunk := await stream.read(128):
                terminal.write(chunk)

        await asyncio.gather(write_to_terminal(process.stdout), write_to_terminal(process.stderr), process.wait())
        button.enable()

    terminal = ui.xterm({'cols': 30, 'rows': 9})
    button = ui.button('Run subprocess', on_click=run_subprocess)


doc.reference(ui.xterm)
