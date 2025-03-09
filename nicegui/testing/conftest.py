import warnings

from .plugin import *  # pylint: disable=wildcard-import,unused-wildcard-import # noqa: F403

# DEPRECATED
warnings.warn('Importing from nicegui.testing.conftest is deprecated. '
              'It will be removed in NiceGUI 3.0. '
              'Use pytest_plugins = ["nicegui.testing.plugin"] instead.', DeprecationWarning, stacklevel=-1)
