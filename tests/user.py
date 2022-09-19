import threading
from asyncio import start_server
from time import sleep

from nicegui import globals as nicegui_globals
from nicegui import ui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class User():

    def __init__(self, selenium: webdriver.Chrome):
        self.selenium = selenium
        self.thread = None

    def start_server(self) -> None:
        '''Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script.'''
        self.thread = threading.Thread(target=ui.run, kwargs={'port': 3392, 'show': False, 'reload': False})
        self.thread.start()
        sleep(1)

    def stop_server(self) -> None:
        '''Stop the webserver.'''
        nicegui_globals.server.should_exit = True
        self.thread.join()

    def open(self, path: str = '/') -> None:
        if self.thread is None:
            self.start_server()
        self.selenium.get('http://localhost:3392' + path)

    def should_see(self, text: str) -> None:
        if text == self.selenium.title:
            return
        assert self.find(text).text == text

    def click(self, target_text: str) -> None:
        self.find(target_text).click()

    def find(self, text: str) -> WebElement:
        return self.selenium.find_element(By.XPATH, f'//*[contains(text(),"{text}")]')
