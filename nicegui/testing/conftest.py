import warnings

from .plugin import *  # pylint: disable=wildcard-import,unused-wildcard-import # noqa: F403

# DEPRECATED
warnings.warn('Importing from nicegui.testing.conftest is deprecated. '
              'Use pytest_plugins = ["nicegui.testing.plugin"] instead.', DeprecationWarning, stacklevel=-1)
