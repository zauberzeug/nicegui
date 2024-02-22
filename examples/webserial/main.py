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
def set_rate(rate):    
    ui.run_javascript(f"writeStream('f{rate}')")    

class App():
    def __init__(self, samp_rate=5, pnts=20):
        self.samp_rate = samp_rate
        self.x = None
        self.y = None
        self.line = None
        self.main_plot = None
        self.pnts = pnts
        self.available = False
        self.connected = False
        self.setup()

    # Build the nicegui UI and initialize plotting area
    def setup(self):
        self.x = np.arange(self.pnts)
        self.y = list(np.zeros(self.pnts))       

        with ui.card().classes("bg-grey-9"):
            with ui.row().classes('w-full justify-center'):
                self.butt_conn = ui.button('Connect', on_click=self.connect)
                self.input_rate = ui.input(label='Rate [Hz]',value=self.samp_rate).props('rounded outlined dense bg-color=yellow-1').classes('w-32').on('keydown.enter', lambda e: set_rate(e.sender.value))
                self.butt_on = ui.button('LED On', on_click=LED_on)
                self.butt_off = ui.button('LED Off', on_click=LED_off)
                self.butt_disconn = ui.button('Disconnect', on_click=self.disconnect)              
                
                self.butt_on.disable()
                self.butt_off.disable()
                self.input_rate.disable()
                self.butt_disconn.disable()
                
            with ui.row():
                self.main_plot = ui.pyplot(figsize=(7, 5))
                with self.main_plot:
                    self.main_plot.fig.patch.set_facecolor('#ffffe6')
                    self.line, = plt.plot(self.x,self.y)
                    ax = plt.gca()
                    ax.set_facecolor('#ffffe6')
                    plt.ylim(0,1023)
                    plt.xticks(np.arange(0, self.pnts, 5))
                    plt.yticks(np.arange(0, 1023, 128))
                    plt.margins(x=0,y=0,tight=True)
                    plt.grid()
                    plt.title("Light Intensity")
                    plt.xlabel("Sample")
                    plt.ylabel("ADC Value")

        #Pipe external JS script into page body
        with open("script.js") as f:
            ui.add_body_html('<script>' + f.read() + '</script>')
        
        ui.query('body').style('background-color: #8c8c8c')
        ui.on('readevent', lambda e: self.update_plot(e.args))
        
    def update_plot(self, new_val):        
        self.y = [*self.y[1:], int(new_val)]
        with self.main_plot:
            self.line.set_ydata(self.y)
    
    def disconnect(self):
        ui.run_javascript('disconnect()')
        self.butt_on.disable()
        self.butt_off.disable()
        self.input_rate.disable()
        self.butt_conn.enable()
        self.butt_disconn.disable()
    
    async def connect(self):
        self.available = await ui.run_javascript('check_compatability()')
        if self.available:
            self.connected = await ui.run_javascript('connect()', timeout=100)
            if self.connected:
                self.butt_on.enable()
                self.butt_off.enable()
                self.input_rate.enable()
                self.butt_conn.disable()
                self.butt_disconn.enable()
                set_rate(self.samp_rate)
                ui.run_javascript('readLoop()')
            else:
                ui.notify('No port selected or availble')
        else:
            ui.notify('WebSerial is not available in this browser!')  


    def run(self,port=5000):
        ui.run(port=port)


app = App()
app.run()

