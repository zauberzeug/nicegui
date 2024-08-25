try:
    from .screen import Screen
except ImportError:
    # we simply define Screen as None if selenium is not installed
    # this allows simpler dependency management when only using the "User" fixture
    class Screen:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError('Selenium dependencies are missing. Please install selenium to use the Screen class.')

        def __getattr__(self, name):
            raise ImportError('Selenium dependencies are missing. Please install selenium to use the Screen class.')

from .user import User
from .user_interaction import UserInteraction

__all__ = [
    'Screen',
    'User',
    'UserInteraction',
]
