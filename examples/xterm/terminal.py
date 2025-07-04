from typing import Callable, Dict, Optional, Union

from nicegui import ui


class Terminal(ui.element,
               component='terminal.js',
               dependencies=['node_modules/@xterm/xterm/lib/xterm.js']):

    def __init__(self, options: Optional[Dict] = None) -> None:
        """Terminal

        An element that integrates `xterm` to emulate a terminal.
        Note: This element provides only a front-end component without an underlying shell.
        """
        super().__init__()
        self._props['options'] = options or {}

    def on_data(self, callback: Callable[[bytes], None]) -> None:
        """Add a callback to be invoked when data is received from the terminal."""
        self.on('data', lambda event: callback(str(event.args).encode()))

    def write(self, data: Union[bytes, str]) -> None:
        """Write data to the terminal."""
        if isinstance(data, bytes):
            # Xterm.js accepts an `Uint8Array`, which we can get by converting `bytes` to a `list`
            self.run_method('write', list(data))
        else:
            self.run_method('write', data)
