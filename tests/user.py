import threading
import time

from nicegui import globals, ui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

PORT = 3392
IGNORED_CLASSES = ['row', 'column', 'q-field', 'q-field__label', 'q-input']


class User():

    def __init__(self, selenium: webdriver.Chrome) -> None:
        self.selenium = selenium
        self.server_thread = None

    def start_server(self) -> None:
        '''Start the webserver in a separate thread. This is the equivalent of `ui.run()` in a normal script.'''
        self.server_thread = threading.Thread(target=ui.run, kwargs={'port': PORT, 'show': False, 'reload': False})
        self.server_thread.start()

    def stop_server(self) -> None:
        '''Stop the webserver.'''
        self.selenium.close()
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

    def should_see(self, text: str) -> None:
        assert text in self.page(), f'Could not find "{text}" on:\n{self.page()}'

    def click(self, target_text: str) -> None:
        self.find(target_text).click()

    def find(self, text: str) -> WebElement:
        try:
            return self.selenium.find_element_by_xpath(f'//*[contains(text(),"{text}")]')
        except NoSuchElementException:
            raise AssertionError(f'Could not find "{text}" on:\n{self.page()}')

    def page(self) -> str:
        return f'Title: {self.selenium.title}\n\n' + self.content(self.selenium.find_element_by_tag_name('body'))

    def content(self, element: WebElement, indent: str = '') -> str:
        content = ''
        classes: list[str] = []
        for child in element.find_elements_by_xpath('./*'):
            is_element = False
            is_group = False
            render_children = True
            assert isinstance(child, WebElement)
            if not child.find_elements_by_xpath('./*') and child.text:
                is_element = True
                content += f'{indent}{child.text}'
            classes = child.get_attribute('class').strip().split()
            if classes:
                if classes[0] in ['row', 'column']:
                    content += classes[0]
                    is_element = True
                    is_group = True
                if classes[0] == 'q-field':
                    try:
                        name = child.find_element_by_class_name('q-field__label').text
                    except NoSuchElementException:
                        name = ''
                    input = child.find_element_by_tag_name('input')
                    value = input.get_attribute('value') or input.get_attribute('placeholder')
                    content += f'{indent}{name}: {value}'
                    render_children = False
                    is_element = True
                [classes.remove(c) for c in IGNORED_CLASSES if c in classes]
                for i, c in enumerate(classes):
                    classes[i] = c.removeprefix('q-field--')
                if is_element:
                    content += f' [class: {" ".join(classes)}]'
            if is_element:
                content += '\n'
            if render_children:
                content += self.content(child, indent + ('  ' if is_group else ''))
        return content

    def get_tags(self, name: str) -> list[WebElement]:
        return self.selenium.find_elements_by_tag_name(name)

    def get_attributes(self, tag: str, attribute: str) -> list[str]:
        return [t.get_attribute(attribute) for t in self.get_tags(tag)]

    def sleep(self, t: float) -> None:
        time.sleep(t)
