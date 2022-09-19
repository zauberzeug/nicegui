import threading
from time import sleep

from nicegui import globals as nicegui_globals
from nicegui import ui


class Server():

    def start(self):
        '''Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script.'''
        self.thread = threading.Thread(target=ui.run, kwargs={'port': 3392, 'show': False, 'reload': False})
        self.thread.start()
        sleep(1)

    def stop(self):
        '''Stop the webserver.'''
        nicegui_globals.server.should_exit = True
        self.thread.join()

    @property
    def base_url(self):
        return 'http://localhost:3392'
