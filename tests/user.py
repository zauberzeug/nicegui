import logging
import threading
import time

from nicegui import globals as nicegui_globals
from nicegui import ui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class User():

    def __init__(self, selenium: webdriver.Chrome) -> None:
        self.selenium = selenium
        self.thread = None

    def start_server(self) -> None:
        '''Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script.'''
        self.thread = threading.Thread(target=ui.run, kwargs={'port': 3392, 'show': False, 'reload': False})
        self.thread.start()

    def stop_server(self) -> None:
        '''Stop the webserver.'''
        self.selenium.close()
        nicegui_globals.server.should_exit = True
        self.thread.join()

    def open(self, path: str) -> None:
        if self.thread is None:
            self.start_server()
        start = time.time()
        while True:
            try:
                self.selenium.get(f'http://localhost:3392{path}')
                break
            except Exception:
                if time.time() - start > 3:
                    raise
                time.sleep(0.1)
                if not self.thread.is_alive():
                    raise RuntimeError('The NiceGUI server has stopped running')
                logging.warning(f'Failed to open page at {path}, retrying...')

    def should_see(self, text: str) -> None:
        assert self.selenium.title == text or self.find(text).text == text

    def click(self, target_text: str) -> None:
        self.find(target_text).click()

    def find(self, text: str) -> WebElement:
        try:
            return self.selenium.find_element(By.XPATH, f'//*[contains(text(),"{text}")]')
        except NoSuchElementException:
            raise AssertionError(f'Could not find "{text}" on:\n{self.get_body()}')

    def get_body(self) -> str:
        return self.selenium.find_element(By.TAG_NAME, 'body').text
