import os
import threading
import time
from contextlib import contextmanager
from typing import List

import pytest
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException, NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from nicegui import app, globals, ui  # pylint: disable=redefined-builtin

from .test_helpers import TEST_DIR


class Screen:
    PORT = 3392
    IMPLICIT_WAIT = 4
    SCREENSHOT_DIR = TEST_DIR / 'screenshots'

    def __init__(self, selenium: webdriver.Chrome, caplog: pytest.LogCaptureFixture) -> None:
        self.selenium = selenium
        self.caplog = caplog
        self.server_thread = None
        self.ui_run_kwargs = {'port': self.PORT, 'show': False, 'reload': False}
        self.connected = threading.Event()
        app.on_connect(self.connected.set)

    def start_server(self) -> None:
        """Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script."""
        self.server_thread = threading.Thread(target=ui.run, kwargs=self.ui_run_kwargs)
        self.server_thread.start()

    @property
    def is_open(self) -> None:
        # https://stackoverflow.com/a/66150779/3419103
        try:
            self.selenium.current_url  # pylint: disable=pointless-statement
            return True
        except Exception as e:
            print(e)
            return False

    def stop_server(self) -> None:
        """Stop the webserver."""
        self.close()
        self.caplog.clear()
        globals.server.should_exit = True
        self.server_thread.join()

    def open(self, path: str, timeout: float = 3.0) -> None:
        """Try to open the page until the server is ready or we time out.

        If the server is not yet running, start it.
        """
        if self.server_thread is None:
            self.start_server()
        deadline = time.time() + timeout
        self.connected.clear()
        while True:
            try:
                self.selenium.get(f'http://localhost:{self.PORT}{path}')
                self.selenium.find_element(By.XPATH, '//body')  # ensure page and JS are loaded
                self.connected.wait(1)  # Ensure that the client has connected to the API
                break
            except Exception as e:
                if time.time() > deadline:
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
        if self.selenium.title == text:
            return
        self.find(text)

    def wait_for(self, text: str) -> None:
        self.should_contain(text)

    def should_not_contain(self, text: str, wait: float = 0.5) -> None:
        assert self.selenium.title != text
        self.selenium.implicitly_wait(wait)
        with pytest.raises(AssertionError):
            self.find(text)
        self.selenium.implicitly_wait(self.IMPLICIT_WAIT)

    def should_contain_input(self, text: str) -> None:
        deadline = time.time() + self.IMPLICIT_WAIT
        while time.time() < deadline:
            for input_element in self.find_all_by_tag('input'):
                if input_element.get_attribute('value') == text:
                    return
            self.wait(0.1)
        raise AssertionError(f'Could not find input with value "{text}"')

    def click(self, target_text: str) -> WebElement:
        element = self.find(target_text)
        try:
            element.click()
        except ElementNotInteractableException as e:
            raise AssertionError(f'Could not click on "{target_text}" on:\n{element.get_attribute("outerHTML")}') from e
        return element

    def context_click(self, target_text: str) -> WebElement:
        element = self.find(target_text)
        action = ActionChains(self.selenium)
        action.context_click(element).perform()
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
            query = f'//*[not(self::script) and not(self::style) and text()[contains(., "{text}")]]'
            element = self.selenium.find_element(By.XPATH, query)
            try:
                if not element.is_displayed():
                    self.wait(0.1)  # HACK: repeat check after a short delay to avoid timing issue on fast machines
                    if not element.is_displayed():
                        raise AssertionError(f'Found "{text}" but it is hidden')
            except StaleElementReferenceException as e:
                raise AssertionError(f'Found "{text}" but it is hidden') from e
            return element
        except NoSuchElementException as e:
            raise AssertionError(f'Could not find "{text}"') from e

    def find_element(self, element: ui.element) -> WebElement:
        return self.selenium.find_element(By.ID, f'c{element.id}')

    def find_by_class(self, name: str) -> WebElement:
        return self.selenium.find_element(By.CLASS_NAME, name)

    def find_all_by_class(self, name: str) -> WebElement:
        return self.selenium.find_elements(By.CLASS_NAME, name)

    def find_by_tag(self, name: str) -> WebElement:
        return self.selenium.find_element(By.TAG_NAME, name)

    def find_all_by_tag(self, name: str) -> List[WebElement]:
        return self.selenium.find_elements(By.TAG_NAME, name)

    def render_js_logs(self) -> str:
        console = '\n'.join(l['message'] for l in self.selenium.get_log('browser'))
        return f'-- console logs ---\n{console}\n---------------------'

    def get_attributes(self, tag: str, attribute: str) -> List[str]:
        return [t.get_attribute(attribute) for t in self.find_all_by_tag(tag)]

    def wait(self, t: float) -> None:
        time.sleep(t)

    def shot(self, name: str) -> None:
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)
        filename = f'{self.SCREENSHOT_DIR}/{name}.png'
        print(f'Storing screenshot to {filename}')
        self.selenium.get_screenshot_as_file(filename)

    def assert_py_logger(self, level: str, message: str) -> None:
        """Assert that the Python logger has received a message with the given level and text."""
        try:
            assert self.caplog.records, 'Expected a log message'
            record = self.caplog.records[0]
            print(record.levelname, record.message)
            assert record.levelname.strip() == level, f'Expected "{level}" but got "{record.levelname}"'
            assert record.message.strip() == message, f'Expected "{message}" but got "{record.message}"'
        finally:
            self.caplog.records.clear()

    @contextmanager
    def implicitly_wait(self, t: float) -> None:
        self.selenium.implicitly_wait(t)
        yield
        self.selenium.implicitly_wait(self.IMPLICIT_WAIT)
