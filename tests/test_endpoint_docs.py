import requests

from nicegui import __version__

from .screen import Screen


def test_endpoint_documentation_default(screen: Screen):
    screen.open('/')

    response = requests.get(f'http://localhost:{Screen.PORT}/openapi.json')
    assert set(response.json()['paths']) == set()


def test_endpoint_documentation_page_only(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'page'
    screen.open('/')

    response = requests.get(f'http://localhost:{Screen.PORT}/openapi.json')
    assert set(response.json()['paths']) == {'/'}


def test_endpoint_documentation_internal_only(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'internal'
    screen.open('/')

    response = requests.get(f'http://localhost:{Screen.PORT}/openapi.json')
    assert set(response.json()['paths']) == {
        f'/_nicegui/{__version__}/libraries/{{key}}',
        f'/_nicegui/{__version__}/components/{{key}}',
    }


def test_endpoint_documentation_all(screen: Screen):
    screen.ui_run_kwargs['endpoint_documentation'] = 'all'
    screen.open('/')

    response = requests.get(f'http://localhost:{Screen.PORT}/openapi.json')
    assert set(response.json()['paths']) == {
        '/',
        f'/_nicegui/{__version__}/libraries/{{key}}',
        f'/_nicegui/{__version__}/components/{{key}}',
    }
