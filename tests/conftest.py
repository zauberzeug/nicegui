import os

os.environ.setdefault('MPLBACKEND', 'Agg')  # NOTE: force a non-GUI Matplotlib backend during tests

pytest_plugins = ['nicegui.testing.plugin']
