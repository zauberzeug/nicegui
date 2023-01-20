from pathlib import Path
from typing import List

from selenium.webdriver.common.by import By

from nicegui import events, ui

from .screen import Screen

test_path1 = Path('tests/test_upload.py').resolve()
test_path2 = Path('tests/test_scene.py').resolve()


def test_uploading_text_file(screen: Screen):
    results: List[events.UploadEventArguments] = []
    ui.upload(on_upload=results.append, label='Test Title')

    screen.open('/')
    screen.should_contain('Test Title')
    screen.selenium.find_element(By.CLASS_NAME, 'q-uploader__input').send_keys(str(test_path1))
    screen.wait(0.1)
    screen.selenium.find_elements(By.CLASS_NAME, 'q-btn')[1].click()
    screen.wait(0.1)
    assert len(results) == 1
    assert results[0].name == test_path1.name
    assert results[0].type in {'text/x-python', 'text/x-python-script'}
    assert results[0].content.read() == test_path1.read_bytes()


def test_two_upload_elements(screen: Screen):
    results: List[events.UploadEventArguments] = []
    ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 1')
    ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 2')

    screen.open('/')
    screen.should_contain('Test Title 1')
    screen.should_contain('Test Title 2')
    screen.selenium.find_element(By.CLASS_NAME, 'q-uploader__input').send_keys(str(test_path1))
    screen.selenium.find_elements(By.CLASS_NAME, 'q-uploader__input')[1].send_keys(str(test_path2))
    screen.wait(0.1)
    assert len(results) == 2
    assert results[0].name == test_path1.name
    assert results[1].name == test_path2.name


def test_uploading_from_two_tabs(screen: Screen):
    @ui.page('/')
    def page():
        ui.upload(on_upload=lambda e: ui.label(f'uploaded {e.name}'), auto_upload=True)

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_not_contain(test_path1.name)
    screen.selenium.find_element(By.CLASS_NAME, 'q-uploader__input').send_keys(str(test_path1))
    screen.wait(0.3)
    screen.should_contain(f'uploaded {test_path1.name}')
    screen.switch_to(0)
    screen.should_not_contain(f'uploaded {test_path1.name}')
