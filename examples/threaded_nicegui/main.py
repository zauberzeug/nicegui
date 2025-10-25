#!/usr/bin/env python3
import threading

from nicegui import Event, app, ui


class GUI:
    """Encapsulates NiceGUI in a separate thread with Event-based communication.

    This pattern is useful for any scenario where the main thread needs to remain available for other work.
    """

    def __init__(self) -> None:
        self.message = Event[str]()  # NOTE: broadcast data to all clients currently visiting self.root

    def start(self) -> None:
        """Start the NiceGUI server in a separate thread."""
        started = threading.Event()
        app.on_startup(started.set)
        thread = threading.Thread(target=lambda: ui.run(self.root, reload=False), daemon=True)
        thread.start()
        if not started.wait(timeout=3.0):  # NOTE: wait for the server to start
            raise RuntimeError('NiceGUI did not start within 3 seconds.')

    def root(self) -> None:
        """Create the UI for each new visitor."""
        ui.label('NiceGUI running in separate thread').classes('text-h6')
        message_label = ui.label('Waiting for CLI input...')
        self.message.subscribe(message_label.set_text)


if __name__ == '__main__':
    gui = GUI()
    gui.start()
    print('Type messages to update website from the main thread (or "quit" to exit).\n')
    try:
        while (user_input := input('> ')) != 'quit':
            gui.message.emit(user_input)
    except (EOFError, KeyboardInterrupt):
        pass
