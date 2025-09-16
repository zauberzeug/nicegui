from pathlib import Path
from typing import List

import pytest

from nicegui import events, ui
from nicegui.testing import Screen

test_path1 = Path('tests/test_upload.py').resolve()
test_path2 = Path('tests/test_scene.py').resolve()


def test_uploading_text_file(screen: Screen):
    results: List[events.UploadEventArguments] = []
    ui.upload(on_upload=results.append, label='Test Title')

    screen.open('/')
    screen.should_contain('Test Title')
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.wait(0.1)
    screen.click('cloud_upload')
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
    screen.find_all_by_class('q-uploader__input')[0].send_keys(str(test_path1))
    screen.find_all_by_class('q-uploader__input')[1].send_keys(str(test_path2))
    screen.wait(0.1)
    assert len(results) == 2
    assert results[0].name == test_path1.name
    assert results[1].name == test_path2.name


@pytest.mark.filterwarnings('ignore::pytest.PytestUnraisableExceptionWarning')
def test_uploading_from_two_tabs(screen: Screen):
    @ui.page('/')
    def page():
        ui.upload(on_upload=lambda e: ui.label(f'uploaded {e.name}'), auto_upload=True)

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_not_contain(test_path1.name)
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.should_contain(f'uploaded {test_path1.name}')
    screen.switch_to(0)
    screen.should_not_contain(f'uploaded {test_path1.name}')


def test_upload_with_header_slot(screen: Screen):
    with ui.upload().add_slot('header'):
        ui.label('Header')

    screen.open('/')
    screen.should_contain('Header')


def test_replace_upload(screen: Screen):
    with ui.row() as container:
        ui.upload(label='A')

    def replace():
        container.clear()
        with container:
            ui.upload(label='B')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')
    screen.click('Replace')
    screen.wait(0.5)
    screen.should_contain('B')
    screen.should_not_contain('A')


def test_reset_upload(screen: Screen):
    upload = ui.upload()
    ui.button('Reset', on_click=upload.reset)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.should_contain(test_path1.name)
    screen.click('Reset')
    screen.wait(0.5)
    screen.should_not_contain(test_path1.name)


def test_multi_upload_event(screen: Screen):
    results: List[events.MultiUploadEventArguments] = []
    ui.upload(on_multi_upload=results.append, multiple=True)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(f'{test_path1}\n{test_path2}')
    screen.wait(0.1)
    screen.click('cloud_upload')
    screen.wait(0.1)

    assert len(results) == 1
    assert results[0].names == [test_path1.name, test_path2.name]
    assert results[0].contents[0].read() == test_path1.read_bytes()
    assert results[0].contents[1].read() == test_path2.read_bytes()
