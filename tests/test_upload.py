import asyncio
import gc
import tempfile
import weakref
from io import BytesIO
from pathlib import Path

import httpx
import pytest
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartParser

from nicegui import app, events, ui
from nicegui.elements.upload_files import _sanitize_filename, create_file_upload
from nicegui.testing import Screen, User

test_path1 = Path('tests/test_upload.py').resolve()
test_path2 = Path('tests/test_scene.py').resolve()


async def test_deleted_uploads_are_collectable(user: User):
    uploads = []

    @ui.page('/')
    def page():
        uploads.append(weakref.ref(ui.upload()))

    for _ in range(4):
        client = await user.open('/')
        client.delete()
        await asyncio.sleep(0)
    gc.collect()
    assert all(upload() is None for upload in uploads)


async def test_upload_route_count_is_constant(user: User):
    @ui.page('/')
    def page():
        pass

    client = await user.open('/')
    route_count = len(app.routes)
    for count in (1, 10, 10):
        with client:
            uploads = [ui.upload() for _ in range(count)]
        assert len(app.routes) == route_count
        for upload in uploads:
            upload.delete()
        assert len(app.routes) == route_count


async def test_upload_requests_are_isolated(user: User):
    uploads = []
    results = []

    @ui.page('/')
    def page():
        for _ in range(2):
            uploads.append(ui.upload(on_upload=lambda e: results.append((e.sender, e.file.name))))

    first = await user.open('/')
    second = await user.open('/')
    assert uploads[0].id == uploads[2].id  # the client ID must disambiguate identical element IDs
    for index, upload in enumerate(uploads):
        response = await user.http_client.post(upload.props['url'], files={'file': (f'{index}.txt', b'test')})
        assert response.status_code == 200
        assert response.json() == {'upload': 'success'}
        assert results[-1] == (upload, f'{index}.txt')
    first.delete()
    response = await user.http_client.post(uploads[0].props['url'], files={'file': ('stale.txt', b'test')})
    assert response.status_code == 404
    response = await user.http_client.post(uploads[2].props['url'], files={'file': ('live.txt', b'test')})
    assert response.status_code == 200
    assert results[-1] == (uploads[2], 'live.txt')
    second.delete()


@pytest.mark.parametrize('target', ['missing_client', 'missing_element', 'wrong_type', 'malformed', 'deleted'])
async def test_invalid_upload_target(user: User, target: str):
    elements = []
    results = []

    @ui.page('/')
    def page():
        elements.extend([ui.upload(on_upload=results.append), ui.label('Not an upload')])

    client = await user.open('/')
    upload = elements[0]
    client_id = 'missing' if target == 'missing_client' else client.id
    element_id = {'missing_element': '-1',
                  'wrong_type': str(elements[1].id), 'malformed': 'invalid'}.get(target, str(upload.id))
    if target == 'deleted':
        upload.delete()
    response = await user.http_client.post(f'/_nicegui/client/{client_id}/upload/{element_id}',
                                           files={'file': ('test.txt', b'test')})
    assert response.status_code == (422 if target == 'malformed' else 404)
    assert not results


def test_uploads_are_collectable_after_reload(screen: Screen):
    uploads = []

    @ui.page('/', reconnect_timeout=1)
    def page():
        uploads.append(weakref.ref(ui.upload(label='Upload')))

    screen.open('/')
    for _ in range(3):
        screen.should_contain('Upload')
        screen.selenium.refresh()
    screen.should_contain('Upload')
    screen.wait(5)
    gc.collect()
    assert len(uploads) == 4
    assert sum(upload() is not None for upload in uploads) == 1


async def test_uploading_text_file(screen: Screen):
    results: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_upload=results.append, label='Test Title')

    screen.open('/')
    screen.should_contain('Test Title')
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.wait(0.1)
    screen.click('cloud_upload')
    screen.wait(0.1)
    assert len(results) == 1
    assert results[0].file.name == test_path1.name
    assert results[0].file.content_type in {'text/x-python', 'text/x-python-script'}
    assert await results[0].file.read() == test_path1.read_bytes()


@pytest.mark.parametrize('state', ['enabled', 'disabled', 'hidden'])
def test_upload_route_respects_disabled_and_hidden_state(screen: Screen, state: str):
    results: list[events.UploadEventArguments] = []
    upload: ui.upload = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal upload
        upload = ui.upload(on_upload=results.append, label='Test Title')
        if state == 'disabled':
            upload.disable()
        if state == 'hidden':
            upload.set_visibility(False)

    screen.open('/')
    with httpx.Client() as http_client:
        response = http_client.post(f'http://localhost:{Screen.PORT}{upload.props["url"]}',
                                    files={'file': ('test.txt', b'content')})
    assert response.status_code == (200 if state == 'enabled' else 403)
    assert len(results) == (1 if state == 'enabled' else 0)


def test_two_upload_elements(screen: Screen):
    results: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 1')
        ui.upload(on_upload=results.append, auto_upload=True, label='Test Title 2')

    screen.open('/')
    screen.should_contain('Test Title 1')
    screen.should_contain('Test Title 2')
    screen.find_all_by_class('q-uploader__input')[0].send_keys(str(test_path1))
    screen.find_all_by_class('q-uploader__input')[1].send_keys(str(test_path2))
    screen.wait(0.1)
    assert len(results) == 2
    assert results[0].file.name == test_path1.name
    assert results[1].file.name == test_path2.name


def test_uploading_from_two_tabs(screen: Screen):
    @ui.page('/')
    def page():
        ui.upload(on_upload=lambda e: ui.label(f'uploaded {e.file.name}'), auto_upload=True)

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_not_contain(test_path1.name)
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.should_contain(f'uploaded {test_path1.name}')
    screen.switch_to(0)
    screen.should_not_contain(f'uploaded {test_path1.name}')


def test_upload_with_header_slot(screen: Screen):
    @ui.page('/')
    def page():
        with ui.upload().add_slot('header'):
            ui.label('Header')

    screen.open('/')
    screen.should_contain('Header')


def test_replace_upload(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.upload(label='A')

        def replace():
            with container.clear():
                ui.upload(label='B')
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')

    screen.click('Replace')
    screen.wait(0.5)
    screen.should_contain('B')
    screen.should_not_contain('A')


async def test_deleting_upload_with_custom_url(user: User):
    @app.post('/custom/upload')
    def custom_upload() -> None:
        pass

    upload: ui.upload = None  # type: ignore[assignment]

    @ui.page('/')
    def page():
        nonlocal upload
        upload = ui.upload().props('url=/custom/upload')

    client = await user.open('/')
    original_url = f'/_nicegui/client/{client.id}/upload/{upload.id}'
    assert (await user.http_client.post(original_url)).status_code == 200
    assert (await user.http_client.post('/custom/upload')).status_code == 200
    upload.delete()
    assert (await user.http_client.post(original_url)).status_code == 404
    assert (await user.http_client.post('/custom/upload')).status_code == 200


def test_reset_upload(screen: Screen):
    @ui.page('/')
    def page():
        upload = ui.upload()
        ui.button('Reset', on_click=upload.reset)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.should_contain(test_path1.name)
    screen.click('Reset')
    screen.wait(0.5)
    screen.should_not_contain(test_path1.name)


async def test_multi_upload_event(screen: Screen):
    results: list[events.MultiUploadEventArguments] = []

    @ui.page('/')
    def page():
        ui.upload(on_multi_upload=results.append, multiple=True)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(f'{test_path1}\n{test_path2}')
    screen.wait(0.1)
    screen.click('cloud_upload')
    screen.wait(0.1)

    assert len(results) == 1
    assert len(results[0].files) == 2
    assert results[0].files[0].name == test_path1.name
    assert results[0].files[1].name == test_path2.name
    assert await results[0].files[0].read() == test_path1.read_bytes()
    assert await results[0].files[1].read() == test_path2.read_bytes()


async def test_two_handlers_can_read_file(screen: Screen):
    reads: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        upload = ui.upload(auto_upload=True)
        upload.on_upload(reads.append)
        upload.on_upload(reads.append)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(str(test_path1))
    screen.wait(0.1)

    assert len(reads) == 2
    upload_1 = await reads[0].file.text()
    upload_2 = await reads[1].file.text()
    assert upload_1 == upload_2 == test_path1.read_text(encoding='utf-8')


@pytest.mark.parametrize('size', [500, 5_000_000])
async def test_different_file_sizes(screen: Screen, size: int, tmp_path: Path):
    tmp_file = tmp_path / 'test.txt'
    reads: list[events.UploadEventArguments] = []

    @ui.page('/')
    def page():
        upload = ui.upload(auto_upload=True)
        upload.on_upload(reads.append)

    tmp_file.write_text('x' * size)

    screen.open('/')
    screen.find_by_class('q-uploader__input').send_keys(str(tmp_file))
    screen.wait(0.1)
    assert reads[0].file.size() == size
    assert await reads[0].file.text() == tmp_file.read_text()


@pytest.mark.parametrize('input_name,expected', [
    ('simple.txt', 'simple.txt'),
    ('../../etc/passwd', 'passwd'),
    ('..\\..\\windows\\evil.exe', 'evil.exe'),
    ('../..\\..\\mixed/traversal\\payload.txt', 'payload.txt'),
    ('', ''),
    (None, ''),
])
def test_upload_filename_sanitization(input_name: str | None, expected: str):
    assert _sanitize_filename(input_name) == expected


async def test_spilled_temp_file_cleaned_up_on_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setattr(MultiPartParser, 'spool_max_size', 8)  # spill to a temp file after the first chunk
    monkeypatch.setattr(tempfile, 'tempdir', str(tmp_path))

    class FlakyUpload(UploadFile):  # one chunk (triggers the spill), then errors mid-upload
        _read = False

        async def read(self, size: int = -1) -> bytes:
            if self._read:
                assert any(tmp_path.iterdir()), 'first chunk should have been spilled to the temp directory'
                raise OSError('No space left on device')
            self._read = True
            return b'x' * 16

    with pytest.raises(OSError):
        await create_file_upload(FlakyUpload(BytesIO(b''), filename='big.bin'), chunk_size=16)

    assert not any(tmp_path.iterdir()), 'spilled temp file should be removed when the upload fails'
