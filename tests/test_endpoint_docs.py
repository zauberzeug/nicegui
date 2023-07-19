from nicegui import ui, __version__ as version

import requests
from .screen import PORT, Screen


def test_endpoint_documentation_default(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.ui_run_kwargs['endpoint_documentation'] = ''
    screen.open('/openapi.json')

    response = requests.get(f'http://localhost:{PORT}/openapi.json')
    assert response.status_code == 200

    schema = response.json()
    assert len(schema['paths']) == 0
    assert schema['paths'] == {}


def test_endpoint_documentation_page_only(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.ui_run_kwargs['endpoint_documentation'] = 'page'
    screen.open('/openapi.json')

    response = requests.get(f'http://localhost:{PORT}/openapi.json')
    assert response.status_code == 200

    schema = response.json()
    assert len(schema['paths']) == 1
    assert '/' in schema['paths']


def test_endpoint_documentation_internal_only(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.ui_run_kwargs['endpoint_documentation'] = 'internal'
    screen.open('/openapi.json')

    response = requests.get(f'http://localhost:{PORT}/openapi.json')
    assert response.status_code == 200

    schema = response.json()
    assert len(schema['paths']) == 2
    assert '/' not in schema['paths']
    assert f'/_nicegui/{version}/libraries/{{key}}' in schema['paths']
    assert f'/_nicegui/{version}/components/{{key}}' in schema['paths']


def test_endpoint_documentation_internal_all(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    screen.ui_run_kwargs['endpoint_documentation'] = 'all'
    screen.open('/openapi.json')

    response = requests.get(f'http://localhost:{PORT}/openapi.json')
    assert response.status_code == 200

    schema = response.json()
    assert len(schema['paths']) == 3
    assert '/' in schema['paths']
    assert f'/_nicegui/{version}/libraries/{{key}}' in schema['paths']
    assert f'/_nicegui/{version}/components/{{key}}' in schema['paths']
