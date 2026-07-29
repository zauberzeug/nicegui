import os

os.environ.setdefault('MPLBACKEND', 'Agg')  # force a non-GUI Matplotlib backend during tests

pytest_plugins = ['nicegui.testing.plugin']


def pytest_collection_modifyitems(items) -> None:
    for item in items:
        if 'screen' in getattr(item, 'fixturenames', ()):
            item.add_marker('screen')
