import os
import threading
import time
from typing import List

import pytest
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from nicegui import globals, ui

PORT = 3392
IGNORED_CLASSES = ['row', 'column', 'q-card', 'q-field', 'q-field__label', 'q-input']


class Screen:
    IMPLICIT_WAIT = 4
    SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screenshots')
    UI_RUN_KWARGS = {'port': PORT, 'show': False, 'reload': False}

    def __init__(self, selenium: webdriver.Chrome, caplog: pytest.LogCaptureFixture) -> None:
        self.selenium = selenium
        self.caplog = caplog
        self.server_thread = None

    def start_server(self) -> None:
        '''Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script.'''
        self.server_thread = threading.Thread(target=ui.run, kwargs=self.UI_RUN_KWARGS)
        self.server_thread.start()

    @property
    def is_open(self) -> None:
        # https://stackoverflow.com/a/66150779/3419103
        try:
            self.selenium.current_url
            return True
        except Exception:
            return False

    def stop_server(self) -> None:
        '''Stop the webserver.'''
        self.close()
        self.caplog.clear()
        globals.server.should_exit = True
        self.server_thread.join()

    def open(self, path: str) -> None:
        if self.server_thread is None:
            self.start_server()
        start = time.time()
        while True:
            try:
                self.selenium.get(f'http://localhost:{PORT}{path}')
                break
            except Exception as e:
                if time.time() - start > 3:
                    raise
                time.sleep(0.1)
                if not self.server_thread.is_alive():
                    raise RuntimeError('The NiceGUI server has stopped running') from e

    def close(self) -> None:
        if self.is_open:
            self.selenium.close()

    def switch_to(self, tab_id: int) -> None:
        window_count = len(self.selenium.window_handles)
        if tab_id > window_count:
            raise IndexError(f'Could not go to or create tab {tab_id}, there are only {window_count} tabs')
        elif tab_id == window_count:
            self.selenium.switch_to.new_window('tab')
        else:
            self.selenium.switch_to.window(self.selenium.window_handles[tab_id])

    def should_contain(self, text: str) -> None:
        assert self.selenium.title == text or self.find(text), f'could not find "{text}"'

    def should_not_contain(self, text: str) -> None:
        assert self.selenium.title != text
        with pytest.raises(AssertionError):
            self.selenium.implicitly_wait(0.5)
            self.find(text)
            self.selenium.implicitly_wait(2)

    def click(self, target_text: str) -> WebElement:
        element = self.find(target_text)
        try:
            element.click()
        except ElementNotInteractableException as e:
            raise AssertionError(f'Could not click on "{target_text}" on:\n{element.get_attribute("outerHTML")}') from e
        return element

    def click_at_position(self, element: WebElement, x: int, y: int) -> None:
        action = ActionChains(self.selenium)
        action.move_to_element_with_offset(element, x, y).click().perform()

    def type(self, text: str) -> None:
        self.selenium.execute_script("window.focus();")
        self.wait(0.2)
        self.selenium.switch_to.active_element.send_keys(text)

    def find(self, text: str) -> WebElement:
        try:
            query = f'//*[not(self::script) and not(self::style) and contains(text(), "{text}")]'
            element = self.selenium.find_element(By.XPATH, query)
            if not element.is_displayed():
                self.wait(0.1)  # HACK: repeat check after a short delay to avoid timing issue on fast machines
                if not element.is_displayed():
                    raise AssertionError(f'Found "{text}" but it is hidden')
            return element
        except NoSuchElementException as e:
            self.selenium.implicitly_wait(0)
            for input in self.selenium.find_elements(By.TAG_NAME, 'input'):
                if input.get_attribute('value') == text:
                    return input
            self.selenium.implicitly_wait(self.IMPLICIT_WAIT)
            raise AssertionError(f'Could not find "{text}"') from e

    def render_js_logs(self) -> str:
        console = '\n'.join(l['message'] for l in self.selenium.get_log('browser'))
        return f'-- console logs ---\n{console}\n---------------------'

    def get_tags(self, name: str) -> List[WebElement]:
        return self.selenium.find_elements(By.TAG_NAME, name)

    def get_attributes(self, tag: str, attribute: str) -> List[str]:
        return [t.get_attribute(attribute) for t in self.get_tags(tag)]

    def wait(self, t: float) -> None:
        time.sleep(t)

    def shot(self, name: str) -> None:
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)
        filename = f'{self.SCREENSHOT_DIR}/{name}.png'
        print(f'Storing screenshot to {filename}')
        self.selenium.get_screenshot_as_file(filename)

    def assert_py_logger(self, level: str, message: str) -> None:
        try:
            assert self.caplog.records, 'Expected a log message'
            record = self.caplog.records[0]
            print(record.levelname, record.message)
            assert record.levelname.strip() == level, f'Expected "{level}" but got "{record.levelname}"'
            assert record.message.strip() == message, f'Expected "{message}" but got "{record.message}"'
        finally:
            self.caplog.records.clear()
