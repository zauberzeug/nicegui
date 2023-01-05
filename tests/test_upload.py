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
