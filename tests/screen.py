import os
import threading
import time
from typing import List

import pytest
from bs4 import BeautifulSoup
from nicegui import globals, ui
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .helper import remove_prefix

PORT = 3392
IGNORED_CLASSES = ['row', 'column', 'q-card', 'q-field', 'q-field__label', 'q-input']


class Screen:
    SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screenshots')
    UI_RUN_KWARGS = {'port': PORT, 'show': False, 'reload': False}

    def __init__(self, selenium: webdriver.Chrome) -> None:
        self.selenium = selenium
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
        except:
            return False

    def stop_server(self) -> None:
        '''Stop the webserver.'''
        self.close()
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
            except Exception:
                if time.time() - start > 3:
                    raise
                time.sleep(0.1)
                if not self.server_thread.is_alive():
                    raise RuntimeError('The NiceGUI server has stopped running')

    def close(self) -> None:
        if self.is_open:
            self.selenium.close()

    def should_contain(self, text: str) -> None:
        assert self.selenium.title == text or self.find(text), \
            f'could not find "{text}" on:\n{self.render_content()}'

    def should_not_contain(self, text: str) -> None:
        assert self.selenium.title != text
        with pytest.raises(AssertionError):
            self.find(text)

    def click(self, target_text: str) -> WebElement:
        element = self.find(target_text)
        try:
            element.click()
        except ElementNotInteractableException:
            raise AssertionError(f'Could not click on "{target_text}" on:\n{element.get_attribute("outerHTML")}')
        return element

    def click_at_position(self, element: WebElement, x: int, y: int) -> None:
        action = ActionChains(self.selenium)
        action.move_to_element_with_offset(element, x, y).click().perform()

    def find(self, text: str) -> WebElement:
        try:
            query = f'//*[not(self::script) and not(self::style) and contains(text(), "{text}")]'
            return self.selenium.find_element(By.XPATH, query)
        except NoSuchElementException:
            raise AssertionError(f'Could not find "{text}" on:\n{self.render_content()}')

    def render_content(self, with_extras: bool = False) -> str:
        body = self.selenium.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
        soup = BeautifulSoup(body, 'html.parser')
        self.simplify_input_tags(soup)
        content = ''
        for child in soup.find_all():
            is_element = False
            if child is None or child.name == 'script':
                continue
            depth = (len(list(child.parents)) - 3) * '  '
            if not child.find_all() and child.text:
                content += depth + child.getText()
                is_element = True
            classes = child.get('class', '')
            if classes:
                if classes[0] in ['row', 'column', 'q-card']:
                    content += depth + remove_prefix(classes[0], 'q-')
                    is_element = True
                if classes[0] == 'q-field':
                    pass
                [classes.remove(c) for c in IGNORED_CLASSES if c in classes]
                for i, c in enumerate(classes):
                    classes[i] = remove_prefix(c, 'q-field--')
                if is_element and with_extras:
                    content += f' [class: {" ".join(classes)}]'

            if is_element:
                content += '\n'

        return f'Title: {self.selenium.title}\n\n{content}'

    def render_html(self) -> str:
        body = self.selenium.page_source
        soup = BeautifulSoup(body, 'html.parser')
        for element in soup.find_all():
            if element.name in ['script', 'style'] and len(element.text) > 10:
                element.string = '... removed lengthy content ...'
        return soup.prettify()

    def render_logs(self) -> str:
        console = '\n'.join(l['message'] for l in self.selenium.get_log('browser'))
        return f'-- console logs ---\n{console}\n---------------------'

    @staticmethod
    def simplify_input_tags(soup: BeautifulSoup) -> None:
        for element in soup.find_all(class_='q-field'):
            new = soup.new_tag('simple_input')
            name = element.find(class_='q-field__label').text
            placeholder = element.find(class_='q-field__native').get('placeholder')
            messages = element.find(class_='q-field__messages')
            value = element.find(class_='q-field__native').get('value')
            new.string = (f'{name}: ' if name else '') + (value or placeholder or '') + \
                (f' \u002A{messages.text}' if messages else '')
            new['class'] = element['class']
            element.replace_with(new)

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
