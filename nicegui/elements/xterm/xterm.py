from pathlib import Path

from typing_extensions import Self

from ...awaitable_response import AwaitableResponse
from ...defaults import DEFAULT_PROP, resolve_defaults
from ...element import Element
from ...events import GenericEventArguments, Handler, XtermBellEventArguments, XtermDataEventArguments, handle_event


class Xterm(Element, component='xterm.js', esm={'nicegui-xterm': 'dist'}):

    @resolve_defaults
    def __init__(self, options: dict | None = DEFAULT_PROP | None) -> None:
        """Xterm

        This element is a wrapper around `xterm.js <https://github.com/xtermjs/xterm.js>`_ to emulate a terminal.
        Note: This element provides only a front-end component without an underlying shell.

        *Added in version 3.1.0*

        :param options: A dictionary of options to configure the terminal, see the
                        `xterm.js documentation <https://xtermjs.org/docs/api/terminal/classes/terminal/#constructor>`_.
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')

        self._props['options'] = options or {}

    async def get_rows(self) -> int:
        """Get the number of rows in the terminal's viewport."""
        return await self.run_method('getRows')

    async def get_columns(self) -> int:
        """Get the number of columns  in the terminal's viewport."""
        return await self.run_method('getColumns')

    def fit(self) -> AwaitableResponse:
        """Fit the terminal to its container.

        This method only resizes the terminal, making the number of rows and columns match the size of the container.
        Note that you might also need to resize the backing pty to match the new size of the terminal.

        :return: AwaitableResponse that can be awaited to wait for the completion of the method call
        """
        return self.run_method('fit')

    def on_bell(self, callback: Handler[XtermBellEventArguments]) -> Self:
        """Add a callback to be invoked when the terminal's bell is triggered."""
        self.on('bell', lambda _: handle_event(callback, XtermBellEventArguments(sender=self, client=self.client)))
        return self

    def on_data(self, callback: Handler[XtermDataEventArguments]) -> Self:
        """Add a callback to be invoked when the user types or pastes into the terminal.

        In a typical setup, this should be passed on to the backing pty.
        """
        def handle_data(e: GenericEventArguments) -> None:
            handle_event(callback, XtermDataEventArguments(sender=self, client=self.client, data=e.args))
        self.on('data', handle_data)
        return self

    def input(self, data: str, *, was_user_input: bool = True) -> AwaitableResponse:
        """Input data to application side.

        The data is treated the same way input typed into the terminal would (i.e. the ``data`` event will fire).
        To write data onto the terminal (e.g. data coming from a pty), use the ``write`` method instead.

        :param data: The data to forward to the application.
        :param was_user_input: Whether the input is genuine user input.
                               This triggers additional behavior like focus or selection clearing.
                               Set this to ``False`` if the data sent should not be treated like user input would,
                               for example passing an escape sequence to the application.

        :return: AwaitableResponse that can be awaited to wait for the completion of the method call
        """
        return self.run_method('input', data, was_user_input)

    def write(self, data: bytes | str) -> AwaitableResponse:
        """Write data to the terminal.

        :param data: The data to write to the terminal.
                     This can either be UTF-8 encoded bytes or a string.

        :return: AwaitableResponse that can be awaited to wait for the completion of the method call
        """
        # Xterm.js accepts an `Uint8Array`, which we can get by converting `bytes` to a `list`
        return self.run_method('write', list(data) if isinstance(data, bytes) else data)

    def writeln(self, data: bytes | str) -> AwaitableResponse:
        """Write data to the terminal, followed by a break line character (``\\n``).

        :param data: The data to write to the terminal.
                     This can either be UTF-8 encoded bytes or a string.

        :return: AwaitableResponse that can be awaited to wait for the completion of the method call
        """
        # Xterm.js accepts an `Uint8Array`, which we can get by converting `bytes` to a `list`
        return self.run_method('writeln', list(data) if isinstance(data, bytes) else data)

    def run_terminal_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a method of the Xterm.js terminal instance.

        Refer to the `Xterm.js documentation <https://xtermjs.org/docs/api/terminal/classes/terminal/#methods>`_
        for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_terminal_method', name, *args, timeout=timeout)
