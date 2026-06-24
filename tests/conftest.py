import os

os.environ.setdefault('MPLBACKEND', 'Agg')  # force a non-GUI Matplotlib backend during tests

pytest_plugins = ['nicegui.testing.plugin']
