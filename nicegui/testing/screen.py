import os
import re
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Generator, List, Optional, Union, overload

import pytest
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from nicegui import app, ui
from nicegui.server import Server


class Screen:
    PORT = 3392
    IMPLICIT_WAIT = 4
    SCREENSHOT_DIR = Path('screenshots')

    def __init__(self, selenium: webdriver.Chrome, caplog: pytest.LogCaptureFixture) -> None:
        self.selenium = selenium
        self.caplog = caplog
        self.server_thread: Optional[threading.Thread] = None
        self.ui_run_kwargs = {'port': self.PORT, 'show': False, 'reload': False}
        self.connected = threading.Event()
        app.on_connect(self.connected.set)

    def start_server(self) -> None:
        """Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script."""
        self.server_thread = threading.Thread(target=ui.run, kwargs=self.ui_run_kwargs)
        self.server_thread.start()

    @property
    def is_open(self) -> bool:
        """Check if the browser is open."""
        # https://stackoverflow.com/a/66150779/3419103
        try:
            self.selenium.current_url  # pylint: disable=pointless-statement # noqa: B018
            return True
        except Exception as e:
            print(e)
            return False

    def stop_server(self) -> None:
        """Stop the webserver."""
        self.close()
        self.caplog.clear()
        Server.instance.should_exit = True
        if self.server_thread:
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
                assert self.server_thread is not None
                if not self.server_thread.is_alive():
                    raise RuntimeError('The NiceGUI server has stopped running') from e

    def close(self) -> None:
        """Close the browser."""
        if self.is_open:
            self.selenium.close()

    def switch_to(self, tab_id: int) -> None:
        """Switch to the tab with the given index, or create it if it does not exist."""
        window_count = len(self.selenium.window_handles)
        if tab_id > window_count:
            raise IndexError(f'Could not go to or create tab {tab_id}, there are only {window_count} tabs')
        if tab_id == window_count:
            self.selenium.switch_to.new_window('tab')
        else:
            self.selenium.switch_to.window(self.selenium.window_handles[tab_id])

    def should_contain(self, text: str) -> None:
        """Assert that the page contains the given text."""
        if self.selenium.title == text:
            return
        self.find(text)

    @overload
    def wait_for(self, target: str) -> None:
        """Wait until the page contains the given text."""

    @overload
    def wait_for(self, target: Callable[..., bool]) -> None:
        """Wait until the given condition is met."""

    def wait_for(self, target: Union[str, Callable[..., bool]]) -> None:
        """Wait until the page contains the given text or the given condition is met."""
        if isinstance(target, str):
            self.should_contain(target)
        if callable(target):
            deadline = time.time() + self.IMPLICIT_WAIT
            while time.time() < deadline:
                if target():
                    return
                self.wait(0.1)
            raise AssertionError('Condition not met')

    def should_not_contain(self, text: str, wait: float = 0.5) -> None:
        """Assert that the page does not contain the given text."""
        assert self.selenium.title != text
        try:
            self.selenium.implicitly_wait(wait)
            with pytest.raises(AssertionError):
                self.find(text)
        finally:
            self.selenium.implicitly_wait(self.IMPLICIT_WAIT)

    def should_contain_input(self, text: str) -> None:
        """Assert that the page contains an input with the given value."""
        deadline = time.time() + self.IMPLICIT_WAIT
        while time.time() < deadline:
            for input_element in self.find_all_by_tag('input'):
                if input_element.get_attribute('value') == text:
                    return
            self.wait(0.1)
        raise AssertionError(f'Could not find input with value "{text}"')

    def should_load_image(self, image: WebElement, *, timeout: float = 2.0) -> None:
        """Assert that the given image has loaded."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            js = 'return arguments[0].naturalWidth > 0 && arguments[0].naturalHeight > 0'
            if self.selenium.execute_script(js, image):
                return
        raise AssertionError(f'Image not loaded: {image.get_attribute("outerHTML")}')

    def click(self, target_text: str) -> WebElement:
        """Click on the element containing the given text."""
        element = self.find(target_text)
        try:
            element.click()
        except ElementNotInteractableException as e:
            raise AssertionError(f'Could not click on "{target_text}" on:\n{element.get_attribute("outerHTML")}') from e
        return element

    def context_click(self, target_text: str) -> WebElement:
        """Right-click on the element containing the given text."""
        element = self.find(target_text)
        action = ActionChains(self.selenium)
        action.context_click(element).perform()
        return element

    def click_at_position(self, element: WebElement, x: int, y: int) -> None:
        """Click on the given element at the given position."""
        action = ActionChains(self.selenium)
        action.move_to_element_with_offset(element, x, y).click().perform()

    def type(self, text: str) -> None:
        """Type the given text into the currently focused element."""
        self.selenium.execute_script('window.focus();')
        self.wait(0.2)
        self.selenium.switch_to.active_element.send_keys(text)

    def find(self, text: str) -> WebElement:
        """Find the element containing the given text."""
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

    def find_all(self, text: str) -> List[WebElement]:
        """Find all elements containing the given text."""
        query = f'//*[not(self::script) and not(self::style) and text()[contains(., "{text}")]]'
        return self.selenium.find_elements(By.XPATH, query)

    def find_element(self, element: ui.element) -> WebElement:
        """Find the given NiceGUI element."""
        return self.selenium.find_element(By.ID, f'c{element.id}')

    def find_by_class(self, name: str) -> WebElement:
        """Find the element with the given CSS class."""
        return self.selenium.find_element(By.CLASS_NAME, name)

    def find_all_by_class(self, name: str) -> List[WebElement]:
        """Find all elements with the given CSS class."""
        return self.selenium.find_elements(By.CLASS_NAME, name)

    def find_by_tag(self, name: str) -> WebElement:
        """Find the element with the given HTML tag."""
        return self.selenium.find_element(By.TAG_NAME, name)

    def find_all_by_tag(self, name: str) -> List[WebElement]:
        """Find all elements with the given HTML tag."""
        return self.selenium.find_elements(By.TAG_NAME, name)

    def find_by_css(self, selector: str) -> WebElement:
        """Find the element with the given CSS selector."""
        return self.selenium.find_element(By.CSS_SELECTOR, selector)

    def render_js_logs(self) -> str:
        """Render the browser console logs as a string."""
        console = '\n'.join(log['message'] for log in self.selenium.get_log('browser'))
        return f'-- console logs ---\n{console}\n---------------------'

    def wait(self, t: float) -> None:
        """Wait for the given number of seconds."""
        time.sleep(t)

    def shot(self, name: str) -> None:
        """Take a screenshot and store it in the screenshots directory."""
        os.makedirs(self.SCREENSHOT_DIR, exist_ok=True)
        filename = f'{self.SCREENSHOT_DIR}/{name}.png'
        print(f'Storing screenshot to {filename}')
        self.selenium.get_screenshot_as_file(filename)

    def assert_py_logger(self, level: str, message: Union[str, re.Pattern]) -> None:
        """Assert that the Python logger has received a message with the given level and text or regex pattern."""
        try:
            assert self.caplog.records, 'Expected a log message'
            record = self.caplog.records[0]
            print(record.levelname, record.message)
            assert record.levelname.strip() == level, f'Expected "{level}" but got "{record.levelname}"'

            if isinstance(message, re.Pattern):
                assert message.search(record.message), f'Expected regex "{message}" but got "{record.message}"'
            else:
                assert record.message.strip() == message, f'Expected "{message}" but got "{record.message}"'
        finally:
            self.caplog.records.clear()

    @contextmanager
    def implicitly_wait(self, t: float) -> Generator[None, None, None]:
        """Temporarily change the implicit wait time."""
        self.selenium.implicitly_wait(t)
        yield
        self.selenium.implicitly_wait(self.IMPLICIT_WAIT)
