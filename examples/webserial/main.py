# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 00:15:05 2024

@author: BA
"""

from nicegui import ui
import numpy as np
from matplotlib import pyplot as plt

# reading a value from JS environment


def get_wariable(var_name):
    return ui.run_javascript(var_name)


def LED_on():
    ui.run_javascript("writeStream('1')")


def LED_off():
    ui.run_javascript("writeStream('0')")




class App():
    def __init__(self, samp_rate=5, pnts=20):
        self.available = False
        self.connected = False
        self.setup()

    # Build the nicegui UI 
    def setup(self):
        with ui.card().classes("bg-grey-9"):
            with ui.column().classes('w-full justify-center'):
                self.butt_conn = ui.button('Connect', on_click=self.connect)                                                                                  
                self.butt_on = ui.button('LED On', on_click=LED_on)
                self.butt_off = ui.button('LED Off', on_click=LED_off)
                self.butt_disconn = ui.button('Disconnect', on_click=self.disconnect)
                self.butt_on.disable()
                self.butt_off.disable()
                self.butt_disconn.disable()
                
        # Pipe external JS script into page body
        with open("script.js") as f:
            ui.add_body_html('<script>' + f.read() + '</script>')

        ui.query('body').style('background-color: #8c8c8c')
        ui.on('readevent', lambda e: self.custom_event(e.args))

    def custom_event(self, counts):
        ui.notify(f"Button pressed {counts} times!")

        
    async def disconnect(self):
        await ui.run_javascript('disconnect()', timeout=5)
        self.butt_on.disable()
        self.butt_off.disable()
        self.butt_disconn.disable()
        self.butt_conn.enable()

    async def connect(self):
        self.available = await ui.run_javascript('check_compatability()')
        if self.available:
            self.connected = await ui.run_javascript('connect()', timeout=100)
            if self.connected:
                self.butt_on.enable()
                self.butt_off.enable()
                self.butt_conn.disable()
                self.butt_disconn.enable()
                ui.run_javascript('readLoop()')
            else:
                ui.notify('No port selected or availble')
        else:
            ui.notify('WebSerial is not available in this browser!')

    def run(self, port=5000):
        ui.run(port=port)


app = App()
app.run()
