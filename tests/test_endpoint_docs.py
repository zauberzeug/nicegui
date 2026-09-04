import httpx
import pytest

from nicegui import __version__, ui
from nicegui.testing import Screen


@pytest.mark.parametrize('endpoint_documentation', ['none', 'page', 'internal', 'all'])
def test_endpoint_documentation(screen: Screen, endpoint_documentation: str):
    screen.ui_run_kwargs['fastapi_docs'] = True
    screen.ui_run_kwargs['endpoint_documentation'] = endpoint_documentation
    uploads: list[ui.upload] = []

    @ui.page('/')
    def page():
        ui.markdown('Hey!')
        uploads.append(ui.upload())

    screen.open('/')
    upload = uploads[0]

    if endpoint_documentation == 'none':
        expected_paths = set()
    elif endpoint_documentation == 'page':
        expected_paths = {'/'}
    elif endpoint_documentation == 'internal':
        expected_paths = {
            f'/_nicegui/{__version__}/libraries/{{key}}',
            f'/_nicegui/{__version__}/components/{{key}}',
            f'/_nicegui/{__version__}/resources/{{key}}/{{path}}',
            f'/_nicegui/{__version__}/dynamic_resources/{{name}}',
            f'/_nicegui/{__version__}/esm/{{key}}/{{path}}',
            f'/_nicegui/client/{upload.client.id}/upload/{upload.id}',
        }
    elif endpoint_documentation == 'all':
        expected_paths = {
            '/',
            f'/_nicegui/{__version__}/libraries/{{key}}',
            f'/_nicegui/{__version__}/components/{{key}}',
            f'/_nicegui/{__version__}/resources/{{key}}/{{path}}',
            f'/_nicegui/{__version__}/dynamic_resources/{{name}}',
            f'/_nicegui/{__version__}/esm/{{key}}/{{path}}',
            f'/_nicegui/client/{upload.client.id}/upload/{upload.id}',
        }
    else:
        raise ValueError(f'Unknown endpoint documentation setting: {endpoint_documentation}')

    assert set(httpx.get(f'http://localhost:{Screen.PORT}/openapi.json', timeout=5).json()['paths']) == expected_paths
