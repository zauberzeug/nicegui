from pathlib import Path

from selenium.webdriver.common.by import By

from nicegui import events, ui

from .screen import Screen


def test_uploading_text_file(screen: Screen):
    result: events.UploadEventArguments = None

    def handle_upload(event: events.UploadEventArguments):
        nonlocal result
        result = event

    ui.upload(on_upload=handle_upload, file_picker_label='Test Title')

    screen.open('/')
    screen.should_contain('Test Title')
    screen.selenium.find_element(By.CLASS_NAME, 'q-uploader__input')\
        .send_keys(str(Path('tests/test_upload.py').resolve()))
    screen.wait(0.1)
    screen.selenium.find_elements(By.CLASS_NAME, 'q-btn')[1].click()
    screen.wait(0.1)
    assert result is not None
    assert result.name == 'test_upload.py'
    assert result.type == 'text/x-python-script'
    assert result.content.read() == Path('tests/test_upload.py').read_bytes()


def test_two_upload_elements(screen: Screen):
    result1: events.UploadEventArguments = None
    result2: events.UploadEventArguments = None

    def handle_upload1(event: events.UploadEventArguments):
        nonlocal result1
        result1 = event

    def handle_upload2(event: events.UploadEventArguments):
        nonlocal result2
        result2 = event

    ui.upload(on_upload=handle_upload1, auto_upload=True, file_picker_label='Test Title 1')
    ui.upload(on_upload=handle_upload2, auto_upload=True, file_picker_label='Test Title 2')

    screen.open('/')
    screen.should_contain('Test Title 1')
    screen.should_contain('Test Title 2')
    screen.selenium.find_element(By.CLASS_NAME, 'q-uploader__input')\
        .send_keys(str(Path('tests/test_upload.py').resolve()))
    screen.selenium.find_elements(By.CLASS_NAME, 'q-uploader__input')[1]\
        .send_keys(str(Path('tests/test_scene.py').resolve()))
    screen.wait(0.1)
    assert result1 is not None
    assert result1.name == 'test_upload.py'
    assert result2 is not None
    assert result2.name == 'test_scene.py'
