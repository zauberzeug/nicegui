import httpx
import pytest

from nicegui import ui
from nicegui.helpers import version_signature
from nicegui.testing import Screen


@pytest.fixture(autouse=True)
def activate_fastapi_docs(screen: Screen):
    screen.ui_run_kwargs['fastapi_docs'] = True


def get_openapi_paths() -> set[str]:
    return set(httpx.get(f'http://localhost:{Screen.PORT}/openapi.json', timeout=5).json()['paths'])


def test_endpoint_documentation_default(screen: Screen):
    @ui.page('/')
    def page():
        ui.markdown('Hey!')

    screen.open('/')
    assert get_openapi_paths() == set()


def test_endpoint_documentation_page_only(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'page'

    @ui.page('/')
    def page():
        ui.markdown('Hey!')

    screen.open('/')
    assert get_openapi_paths() == {'/'}


def test_endpoint_documentation_internal_only(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'internal'

    @ui.page('/')
    def page():
        ui.markdown('Hey!')

    screen.open('/')
    assert get_openapi_paths() == {
        f'/_nicegui/{version_signature()}/libraries/{{key}}',
        f'/_nicegui/{version_signature()}/components/{{key}}',
        f'/_nicegui/{version_signature()}/resources/{{key}}/{{path}}',
        f'/_nicegui/{version_signature()}/dynamic_resources/{{name}}',
        f'/_nicegui/{version_signature()}/esm/{{key}}/{{path}}',
    }


def test_endpoint_documentation_all(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'all'

    @ui.page('/')
    def page():
        ui.markdown('Hey!')

    screen.open('/')
    assert get_openapi_paths() == {
        '/',
        f'/_nicegui/{version_signature()}/libraries/{{key}}',
        f'/_nicegui/{version_signature()}/components/{{key}}',
        f'/_nicegui/{version_signature()}/resources/{{key}}/{{path}}',
        f'/_nicegui/{version_signature()}/dynamic_resources/{{name}}',
        f'/_nicegui/{version_signature()}/esm/{{key}}/{{path}}',
    }
