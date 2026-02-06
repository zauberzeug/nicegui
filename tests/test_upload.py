from pathlib import Path

import pytest

from nicegui import events, ui
from nicegui.testing import SharedScreen

test_path1 = Path('tests/test_upload.py').resolve()
test_path2 = Path('tests/test_scene.py').resolve()


async def test_uploading_text_file(shared_screen: SharedScreen):
    results: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_upload=results.append, label='Test Title')

    shared_screen.open('/')
    shared_screen.should_contain('Test Title')
    shared_screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    shared_screen.wait(0.1)
    shared_screen.click('cloud_upload')
    shared_screen.wait(0.1)
    assert len(results) == 1
    assert results[0].file.name == test_path1.name
    assert results[0].file.content_type in {'text/x-python', 'text/x-python-script'}
    assert await results[0].file.read() == test_path1.read_bytes()


def test_two_upload_elements(shared_screen: SharedScreen):
    results: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 1')
        ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 2')

    shared_screen.open('/')
    shared_screen.should_contain('Test Title 1')
    shared_screen.should_contain('Test Title 2')
    shared_screen.find_all_by_class('q-uploader__input')[0].send_keys(str(test_path1))
    shared_screen.find_all_by_class('q-uploader__input')[1].send_keys(str(test_path2))
    shared_screen.wait(0.1)
    assert len(results) == 2
    assert results[0].file.name == test_path1.name
    assert results[1].file.name == test_path2.name


def test_uploading_from_two_tabs(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.upload(on_upload=lambda e: ui.label(f'uploaded {e.file.name}'), auto_upload=True)

    shared_screen.open('/')
    shared_screen.switch_to(1)
    shared_screen.open('/')
    shared_screen.should_not_contain(test_path1.name)
    shared_screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    shared_screen.should_contain(f'uploaded {test_path1.name}')
    shared_screen.switch_to(0)
    shared_screen.should_not_contain(f'uploaded {test_path1.name}')


def test_upload_with_header_slot(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.upload().add_slot('header'):
            ui.label('Header')

    shared_screen.open('/')
    shared_screen.should_contain('Header')


def test_replace_upload(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.upload(label='A')

        def replace():
            with container.clear():
                ui.upload(label='B')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    shared_screen.should_contain('A')

    shared_screen.click('Replace')
    shared_screen.wait(0.5)
    shared_screen.should_contain('B')
    shared_screen.should_not_contain('A')


def test_reset_upload(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        upload = ui.upload()
        ui.button('Reset', on_click=upload.reset)

    shared_screen.open('/')
    shared_screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    shared_screen.should_contain(test_path1.name)
    shared_screen.click('Reset')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain(test_path1.name)


async def test_multi_upload_event(shared_screen: SharedScreen):
    results: list[events.MultiUploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_multi_upload=results.append, multiple=True)

    shared_screen.open('/')
    shared_screen.find_by_class('q-uploader__input').send_keys(f'{test_path1}\n{test_path2}')
    shared_screen.wait(0.1)
    shared_screen.click('cloud_upload')
    shared_screen.wait(0.1)

    assert len(results) == 1
    assert len(results[0].files) == 2
    assert results[0].files[0].name == test_path1.name
    assert results[0].files[1].name == test_path2.name
    assert await results[0].files[0].read() == test_path1.read_bytes()
    assert await results[0].files[1].read() == test_path2.read_bytes()


async def test_two_handlers_can_read_file(shared_screen: SharedScreen):
    reads: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        upload = ui.upload(auto_upload=True)
        upload.on_upload(reads.append)
        upload.on_upload(reads.append)

    shared_screen.open('/')
    shared_screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    shared_screen.wait(0.1)

    assert len(reads) == 2
    upload_1 = await reads[0].file.text()
    upload_2 = await reads[1].file.text()
    assert upload_1 == upload_2 == test_path1.read_text(encoding='utf-8')


@pytest.mark.parametrize('size', [500, 5_000_000])
async def test_different_file_sizes(shared_screen: SharedScreen, size: int, tmp_path: Path):
    tmp_file = tmp_path / 'test.txt'
    reads: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        upload = ui.upload(auto_upload=True)
        upload.on_upload(reads.append)

    tmp_file.write_text('x' * size)

    shared_screen.open('/')
    shared_screen.find_by_class('q-uploader__input').send_keys(str(tmp_file))
    shared_screen.wait(0.1)
    assert reads[0].file.size() == size
    assert await reads[0].file.text() == tmp_file.read_text()
